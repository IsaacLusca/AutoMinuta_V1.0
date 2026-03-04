import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from .models import MinutaGerada, BlocoPadrao, BlocoDaMinuta, TipoBloco
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright

def editar_minuta_dashboard(request, minuta_id):
    # busca a minuta especificada ou retorna 404 se não existir
    minuta = get_object_or_404(MinutaGerada, id=minuta_id)

    # busca os capitulos padrão (blocos de nível CAPITULO) para exibir na biblioteca
    capitulos_padrao = BlocoPadrao.objects.filter(bloco_pai__isnull=True).order_by('ordem_padrao')

    # busca os blocos da minuta, ordenados pela ordem definida
    blocos_da_minuta = minuta.blocos.order_by('ordem')

    context = {
        'minuta': minuta,
        'capitulos_padrao': capitulos_padrao,
        'blocos_da_minuta': blocos_da_minuta,
    }

    return render(request, 'gerador_avancado/editar_minuta.html', context)

def adicionar_bloco_ajax(request, minuta_id, bloco_padrao_id):
    if request.method == 'POST':
        minuta = get_object_or_404(MinutaGerada, id=minuta_id)
        bloco_origem = get_object_or_404(BlocoPadrao, id=bloco_padrao_id)
        
        # Pega a última ordem do documento
        ultima_ordem = minuta.blocos.aggregate(Max('ordem'))['ordem__max'] or 0
        ordem_atual = ultima_ordem + 10
        
        novo_bloco = BlocoDaMinuta.objects.create(
            minuta=minuta,
            bloco_origem=bloco_origem,
            tipo=bloco_origem.tipo,
            titulo=bloco_origem.titulo,
            conteudo_editado=bloco_origem.conteudo,
            ordem=ordem_atual
        )
        
        filhos = BlocoPadrao.objects.filter(bloco_pai=bloco_origem).order_by('ordem_padrao')
        
        for filho in filhos:
            ordem_atual += 10 
            
            BlocoDaMinuta.objects.create(
                minuta=minuta,
                bloco_origem=filho,
                tipo=filho.tipo,
                titulo=filho.titulo,
                conteudo_editado=filho.conteudo,
                bloco_pai=novo_bloco,
                ordem=ordem_atual
            )
            
        return JsonResponse({'status': 'sucesso'})
    
    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'}, status=400)

def remover_bloco_ajax(request, bloco_minuta_id):
    if request.method == 'POST':
        bloco = get_object_or_404(BlocoDaMinuta, id=bloco_minuta_id)
        bloco.delete()
        return JsonResponse({'status': 'sucesso'})
    
    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'}, status=400)

@csrf_exempt # Para facilitar o salvamento via JS
def salvar_conteudo_bloco_ajax(request, bloco_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        novo_conteudo = data.get('conteudo')
        
        bloco = get_object_or_404(BlocoDaMinuta, id=bloco_id)
        bloco.conteudo_editado = novo_conteudo
        bloco.save()
        
        return JsonResponse({'status': 'sucesso'})
    return JsonResponse({'status': 'erro'}, status=400)

# reordenação dos blocos via drag-and-drop
@csrf_exempt
def reordenar_blocos_ajax(request, minuta_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            itens = data.get('itens', [])
            
            # Garantimos que os blocos pertencem à minuta informada
            for item in itens:
                BlocoDaMinuta.objects.filter(
                    id=item['id'], 
                    minuta_id=minuta_id
                ).update(ordem=item['ordem'])
            
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)
    return JsonResponse({'status': 'erro'}, status=400)

# pré-visualização da minuta (página de visualização sem edição)
def preview_minuta(request, minuta_id):
    # Busca a minuta e seus blocos ordenados
    minuta = get_object_or_404(MinutaGerada, id=minuta_id)
    blocos = minuta.blocos.all().order_by('ordem')

    # busca estrutura dos capitulos
    capitulos_padrao = BlocoPadrao.objects.filter(bloco_pai__isnull=True).order_by('ordem_padrao')

    return render(request, 'gerador_avancado/preview_minuta.html', {
        'minuta': minuta,
        'blocos': blocos,
        'capitulos_padrao': capitulos_padrao,
    })

def gerar_pdf_minuta(request, minuta_id):
    minuta = get_object_or_404(MinutaGerada, id=minuta_id)
    blocos = minuta.blocos.all().order_by('ordem')
    capitulos_padrao = BlocoPadrao.objects.filter(bloco_pai__isnull=True).order_by('ordem_padrao')

    # Renderiza o HTML
    html_string = render_to_string('gerador_avancado/preview_minuta.html', {
        'minuta': minuta,
        'blocos': blocos,
        'capitulos_padrao': capitulos_padrao,
    }, request=request)

    # Usa o Playwright para gerar o PDF perfeitamente
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Carrega o HTML e espera a rede acalmar (para carregar o Bootstrap da CDN)
        page.set_content(html_string, wait_until="networkidle")
        
        # Gera o PDF com margens e numeração nativa do navegador
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "25mm", "bottom": "25mm", "left": "25mm", "right": "25mm"},
            display_header_footer=True,
            header_template="<span></span>", # Cabeçalho vazio por enquanto
            footer_template="<div style='font-size: 10px; width: 100%; text-align: right; padding-right: 25mm; font-family: \"Times New Roman\", serif;'>Página <span class='pageNumber'></span> de <span class='totalPages'></span></div>"
        )
        browser.close()

    # Retorna o PDF para download
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    nome_arquivo = f"Minuta_Edital_{minuta.leilao}_Porto_{minuta.porto}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    
    return response

# No final do seu arquivo views.py
@csrf_exempt
def criar_secao_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titulo = data.get('titulo')
            capitulo_id = data.get('capitulo_id')
            
            if not titulo or not capitulo_id:
                return JsonResponse({'status': 'erro', 'mensagem': 'Título e Capítulo são obrigatórios.'})

            # Busca o capítulo pai
            capitulo_pai = get_object_or_404(BlocoPadrao, id=capitulo_id)
            
            # Descobre qual é a ordem correta para colocar a nova seção no final do capítulo
            ultimo_filho = capitulo_pai.sub_blocos.order_by('-ordem_padrao').first()
            nova_ordem = (ultimo_filho.ordem_padrao + 10) if ultimo_filho else (capitulo_pai.ordem_padrao + 10)
            
            # Cria a nova seção no banco 
            BlocoPadrao.objects.create(
                tipo=TipoBloco.SECAO, # garante que será uma Seção (SE)
                titulo=titulo,
                bloco_pai=capitulo_pai,
                ordem_padrao=nova_ordem
            )
            
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)
    return JsonResponse({'status': 'erro'}, status=400)

@csrf_exempt
def criar_clausula_ajax(request, minuta_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            capitulo_id = data.get('capitulo_id')
            
            minuta = get_object_or_404(MinutaGerada, id=minuta_id)
            capitulo = get_object_or_404(BlocoPadrao, id=capitulo_id)
            
            # cria a referência na Biblioteca (BlocoPadrao)
            nova_clausula_padrao = BlocoPadrao.objects.create(
                tipo='CL', # Ou TipoBloco.CLAUSULA dependendo de como importou
                titulo="",
                conteudo="<p>Nova cláusula (clique para editar)</p>",
                bloco_pai=capitulo,
                ordem_padrao=999 # Vai para o final
            )
            
            # calcula a ordem para o final do documento atual
            ultimo_bloco = minuta.blocos.order_by('-ordem').first()
            nova_ordem = (ultimo_bloco.ordem + 10) if ultimo_bloco else 10
            
            # adiciona a cláusula vazia na Minuta atual
            BlocoDaMinuta.objects.create(
                minuta=minuta,
                bloco_origem=nova_clausula_padrao,
                tipo='CL',
                titulo="",
                conteudo_editado="<p>Nova cláusula (clique para editar)</p>",
                ordem=nova_ordem
            )
            
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)
    return JsonResponse({'status': 'erro'}, status=400)
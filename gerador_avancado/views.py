import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from .models import MinutaGerada, BlocoPadrao, BlocoDaMinuta, TipoBloco
from django.views.decorators.csrf import csrf_exempt

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
        
        # descobre qual é a última 'ordem' no documento do lado direito para colocar este no final
        ultima_ordem = minuta.blocos.aggregate(Max('ordem'))['ordem__max'] or 0
        nova_ordem = ultima_ordem + 10
        
        # cria a cópia do bloco principal (ex: A Seção)
        novo_bloco = BlocoDaMinuta.objects.create(
            minuta=minuta,
            bloco_origem=bloco_origem,
            tipo=bloco_origem.tipo,
            titulo=bloco_origem.titulo,
            conteudo_editado=bloco_origem.conteudo,
            ordem=nova_ordem
        )
        
        # procura se esse bloco tem filhos (ex: As cláusulas dentro da seção)
        filhos = BlocoPadrao.objects.filter(bloco_pai=bloco_origem).order_by('ordem_padrao')
        
        ordem_filho = 10
        for filho in filhos:
            BlocoDaMinuta.objects.create(
                minuta=minuta,
                bloco_origem=filho,
                tipo=filho.tipo,
                titulo=filho.titulo,
                conteudo_editado=filho.conteudo,
                bloco_pai=novo_bloco, # O pai não é mais a biblioteca, é a cópia que acabamos de criar
                ordem=ordem_filho
            )
            ordem_filho += 10
            
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
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from .models import MinutaGerada, BlocoPadrao, BlocoDaMinuta, TipoBloco

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
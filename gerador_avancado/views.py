from django.shortcuts import get_object_or_404, render
from .models import BlocoPadrao, BlocoDaMinuta, MinutaGerada, TipoBloco

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
from django.urls import path
from . import views

urlpatterns = [
    # rota inicial
    path('', views.dashboard_editais, name='dashboard_editais'),
    path('criar-edital/', views.criar_novo_edital, name='criar_novo_edital'),

    # rotas para edição da minuta
    path('minuta/<int:minuta_id>/editar/', views.editar_minuta_dashboard, name='editar_minuta'),
    path('minuta/<int:minuta_id>/adicionar-bloco/<int:bloco_padrao_id>/', views.adicionar_bloco_ajax, name='adicionar_bloco_ajax'),
    path('minuta/remover-bloco/<uuid:bloco_minuta_id>/', views.remover_bloco_ajax, name='remover_bloco_ajax'),
    path('minuta/salvar-bloco/<uuid:bloco_id>/', views.salvar_conteudo_bloco_ajax, name='salvar_conteudo_bloco_ajax'),
    path('minuta/<int:minuta_id>/reordenar/', views.reordenar_blocos_ajax, name='reordenar_blocos_ajax'),
    path('minuta/<int:minuta_id>/preview/', views.preview_minuta, name='preview_minuta'),
    path('minuta/<int:minuta_id>/pdf/', views.gerar_pdf_minuta, name='gerar_pdf_minuta'),
    path('minuta/criar-secao/', views.criar_secao_ajax, name='criar_secao_ajax'),
    path('minuta/<int:minuta_id>/criar-clausula/', views.criar_clausula_ajax, name='criar_clausula_ajax'),
]
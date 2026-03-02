from django.urls import path
from . import views

urlpatterns = [
    path('minuta/<int:minuta_id>/editar/', views.editar_minuta_dashboard, name='editar_minuta'),
    path('minuta/<int:minuta_id>/adicionar-bloco/<int:bloco_padrao_id>/', views.adicionar_bloco_ajax, name='adicionar_bloco_ajax'),
    path('minuta/remover-bloco/<uuid:bloco_minuta_id>/', views.remover_bloco_ajax, name='remover_bloco_ajax'),
]
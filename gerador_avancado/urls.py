from django.urls import path
from . import views

urlpatterns = [
    path('minuta/<int:minuta_id>/editar/', views.editar_minuta_dashboard, name='editar_minuta'),
]
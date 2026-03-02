from django.contrib import admin
from django.urls import path, include  
from gerarMinuta import views

urlpatterns = [
    # Rotas do app antigo (gerarMinuta)
    path("", views.pagina_minutas, name="pagina_minutas"),
    path("gerar/", views.pagina_minutas, name="gerar_minuta_edital"),
    
    path('admin/', admin.site.urls),
    
    path('', include('gerador_avancado.urls')),
]
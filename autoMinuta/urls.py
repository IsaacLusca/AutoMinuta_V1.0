"""
URL configuration for autoMinuta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gerarMinuta import views
from gerarMinuta import editor_views

urlpatterns = [
    # redirecionar para gerar
    path("", views.pagina_minutas, name="pagina_minutas"),
    path('admin/', admin.site.urls),
    path("gerar/", views.pagina_minutas, name="gerar_minuta_edital"),

    # editor estruturado
    path("editor/", editor_views.template_list, name="editor_template_list"),
    path("editor/templates/new/", editor_views.template_create, name="editor_template_create"),
    path("editor/templates/<slug:slug>/", editor_views.template_detail, name="editor_template_detail"),
    path("editor/templates/<slug:slug>/edit/", editor_views.template_edit, name="editor_template_edit"),
    path("editor/placeholders/", editor_views.placeholder_list, name="editor_placeholder_list"),
    path("editor/placeholders/new/", editor_views.placeholder_create, name="editor_placeholder_create"),
    path(
        "editor/templates/<slug:slug>/placeholders/add/",
        editor_views.template_placeholder_add,
        name="editor_template_placeholder_add",
    ),
    path(
        "editor/templates/<slug:slug>/placeholders/<int:binding_id>/remove/",
        editor_views.template_placeholder_remove,
        name="editor_template_placeholder_remove",
    ),
    path("editor/templates/<slug:slug>/sections/new/", editor_views.section_create, name="editor_section_create"),
    path(
        "editor/templates/<slug:slug>/sections/<int:section_id>/edit/",
        editor_views.section_edit,
        name="editor_section_edit",
    ),
    path(
        "editor/templates/<slug:slug>/sections/<int:section_id>/delete/",
        editor_views.section_delete,
        name="editor_section_delete",
    ),
    path(
        "editor/templates/<slug:slug>/sections/<int:section_id>/move/<str:direction>/",
        editor_views.section_move,
        name="editor_section_move",
    ),
    path(
        "editor/templates/<slug:slug>/generate/",
        editor_views.template_generate_docx,
        name="editor_template_generate",
    ),
]

from django.contrib import admin
from .models import MinutaGerada, BlocoPadrao, BlocoDaMinuta

@admin.register(MinutaGerada)
class MinutaGeradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'leilao', 'porto', 'arrendamento', 'criado_em')
    search_fields = ('leilao', 'porto')
    list_filter = ('criado_em',)

@admin.register(BlocoPadrao)
class BlocoPadraoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titulo', 'bloco_pai', 'ordem_padrao', 'obrigatorio')
    list_filter = ('tipo', 'obrigatorio')
    search_fields = ('titulo', 'conteudo')
    ordering = ('bloco_pai', 'ordem_padrao')

@admin.register(BlocoDaMinuta)
class BlocoDaMinutaAdmin(admin.ModelAdmin):
    list_display = ('minuta', 'tipo', 'titulo', 'bloco_pai', 'ordem')
    list_filter = ('tipo', 'minuta')
    search_fields = ('titulo', 'conteudo_editado')
    ordering = ('minuta', 'bloco_pai', 'ordem')
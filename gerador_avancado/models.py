from django.db import models

class TipoBloco(models.TextChoices):
    CAPITULO = 'CA', 'Capítulo'
    SECAO = 'SE', 'Seção'
    SUBSECAO = 'SU', 'Subseção'
    CLAUSULA = 'CL', 'Cláusula'

class BlocoPadrao(models.Model):
    # Parte da esquerda, opções de seção, subseção, cláusula
    tipo = models.CharField(max_length=2, choices=TipoBloco.choices)
    titulo = models.CharField(max_length=255, blank=True, null=True, help_text="Ex: DAS DISPOSIÇÕES INICIAIS")
    conteudo = models.TextField(blank=True, null=True, help_text="Conteúdo editável no CKEditor. Pode ser vazio para Capítulos.")

    # Blocos que podem pertencer/referenciar outros blocos
    bloco_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_blocos')
    ordem_padrao = models.PositiveIntegerField(default=0, help_text="Ordem de exibição dos blocos. Blocos com ordem menor aparecem primeiro.")

    class Meta:
        ordering = ['ordem_padrao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo or 'Sem título'}"
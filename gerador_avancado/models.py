import uuid

from django.db import models
from ckeditor.fields import RichTextField

class TipoBloco(models.TextChoices):
    CAPITULO = 'CA', 'Capítulo'
    SECAO = 'SE', 'Seção'
    SUBSECAO = 'SU', 'Subseção'
    CLAUSULA = 'CL', 'Cláusula'
    TEXTO = 'TX', 'Texto'
    APENDICE = 'AP', 'Apêndice'

class BlocoPadrao(models.Model):
    # Parte da esquerda, opções de seção, subseção, cláusula
    tipo = models.CharField(max_length=2, choices=TipoBloco.choices)
    titulo = models.CharField(max_length=255, blank=True, null=True, help_text="Ex: DAS DISPOSIÇÕES INICIAIS")
    conteudo = RichTextField(blank=True, null=True, help_text="Conteúdo editável no CKEditor. Pode ser vazio para Capítulos.")

    # Blocos que podem pertencer/referenciar outros blocos
    bloco_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_blocos')
    ordem_padrao = models.PositiveIntegerField(default=0, help_text="Ordem de exibição dos blocos. Blocos com ordem menor aparecem primeiro.")

    obrigatorio = models.BooleanField(default=False, help_text="Indica se o bloco é obrigatório (não pode ser removido da minuta).")

    class Meta:
        ordering = ['ordem_padrao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo or 'Sem título'}"
    
class MinutaGerada(models.Model):
    # Identificar minuta
    nome_interno = models.CharField(max_length=200, default="Novo Rascunho de Edital")

    # Identificação geral
    leilao = models.CharField(max_length=200, blank=True)
    arrendamento = models.CharField(max_length=200, blank=True)
    perfil_da_carga = models.CharField(max_length=200, blank=True)
    cargas_no_mme = models.CharField(max_length=200, blank=True)
    porto = models.CharField(max_length=200, blank=True)
    codigo_area = models.CharField(max_length=200, blank=True)
    poder_concedente = models.CharField(max_length=200, blank=True)

    # Datas do edital
    data_publicacao_edital = models.CharField(max_length=200, blank=True)
    data_secao_recebimento_volume = models.CharField(max_length=200, blank=True)
    data_secao_publica = models.CharField(max_length=200, blank=True)
    data_publicacao_dou_audiencia = models.CharField(max_length=200, blank=True)
    data_realizacao_audiencia = models.CharField(max_length=200, blank=True)
    data_publicacao_dou_consulta_publica = models.CharField(max_length=200, blank=True)
    data_consulta_publica = models.CharField(max_length=200, blank=True)
    data_publicacao_edital_extenso = models.CharField(max_length=200, blank=True)
    data_base = models.CharField(max_length=200, blank=True)

    # Prazos
    prazo_impugnacao = models.CharField(max_length=200, blank=True)
    prazo_solicitacao_esclarecimento = models.CharField(max_length=200, blank=True)
    prazo_divulgacao_decisao_cpla = models.CharField(max_length=200, blank=True)
    prazo_interposicao_recursos = models.CharField(max_length=200, blank=True)

    # Resultados e divulgações
    publicacao_ata_julgamento = models.CharField(max_length=200, blank=True)
    resultado_interposicao_recursos = models.CharField(max_length=200, blank=True)
    data_divulgacao_classificacao_propostas = models.CharField(max_length=200, blank=True)
    data_divulgacao_resultado_final_leilao = models.CharField(max_length=200, blank=True)
    data_divulgacao_ata_impugnacao = models.CharField(max_length=200, blank=True)

    # Informações do leilão
    modalidade_leilao = models.CharField(max_length=200, blank=True)
    tipo_criterio = models.CharField(max_length=200, blank=True)

    # Localização e área
    municipio = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=200, blank=True)
    area_m2 = models.CharField(max_length=200, blank=True)
    area_m2_extenso = models.CharField(max_length=200, blank=True)

    # Arrendamento
    prazo_arrendamento = models.CharField(max_length=200, blank=True)
    prazo_arrendamento_extenso = models.CharField(max_length=200, blank=True)

    # Contato visita técnica
    contato_visita_nome = models.CharField(max_length=200, blank=True)
    contato_visita_cargo = models.CharField(max_length=200, blank=True)
    contato_visita_endereco = models.CharField(max_length=200, blank=True)
    contato_visita_email = models.EmailField(blank=True)

    # Valores financeiros
    valor_garantia = models.CharField(max_length=200, blank=True)
    valor_garantia_extenso = models.CharField(max_length=200, blank=True)
    remuneracao_b3 = models.CharField(max_length=200, blank=True)
    remuneracao_b3_extenso = models.CharField(max_length=200, blank=True)
    remuneracao_estruturadora = models.CharField(max_length=200, blank=True)
    remuneracao_estruturadora_extenso = models.CharField(max_length=200, blank=True)
    remuneracao_ap = models.CharField(max_length=200, blank=True)
    remuneracao_ap_extenso = models.CharField(max_length=200, blank=True)
    valor_capital_social = models.CharField(max_length=200, blank=True)
    valor_capital_social_extenso = models.CharField(max_length=200, blank=True)

    # Períodos
    inicio_esclarecimentos = models.CharField(max_length=200, blank=True)
    fim_esclarecimentos = models.CharField(max_length=200, blank=True)
    inicio_impugnacao = models.CharField(max_length=200, blank=True)
    fim_impugnacao = models.CharField(max_length=200, blank=True)

    # Contrato
    numero_contrato = models.CharField(max_length=200, blank=True)
    ano_contrato = models.CharField(max_length=200, blank=True)
    numero_edital = models.CharField(max_length=200, blank=True)
    numero_processo_administrativo = models.CharField(max_length=200, blank=True)

    # Secretário de Portos
    nome_secretario_portos = models.CharField(max_length=200, blank=True)
    qualificacao_secretario_portos = models.CharField(max_length=200, blank=True)
    decreto_nomeacao_secretario = models.CharField(max_length=200, blank=True)
    data_decreto_secretario = models.CharField(max_length=200, blank=True)
    data_dou_secretario = models.CharField(max_length=200, blank=True)

    # ANTAQ
    nome_diretor_geral_antaq = models.CharField(max_length=200, blank=True)
    qualificacao_diretor_geral_antaq = models.CharField(max_length=200, blank=True)
    ato_designacao_diretor_antaq = models.CharField(max_length=200, blank=True)
    data_dou_diretor_antaq = models.CharField(max_length=200, blank=True)
    nome_segundo_diretor = models.CharField(max_length=200, blank=True)
    ato_designacao_segundo_diretor = models.CharField(max_length=200, blank=True)
    data_dou_segundo_diretor = models.CharField(max_length=200, blank=True)
    sede_antaq = models.CharField(max_length=200, blank=True)

    # Autoridade Portuária
    cnpj_autoridade_portuaria = models.CharField(max_length=200, blank=True)
    nome_diretor_presidente_ap = models.CharField(max_length=200, blank=True)
    qualificacao_diretor_presidente_ap = models.CharField(max_length=200, blank=True)
    ato_designacao_diretor_ap = models.CharField(max_length=200, blank=True)
    data_dou_diretor_ap = models.CharField(max_length=200, blank=True)
    sede_autoridade_portuaria = models.CharField(max_length=200, blank=True)

    # Arrendatária
    nome_arrendataria = models.CharField(max_length=200, blank=True)
    tipo_sociedade_arrendataria = models.CharField(max_length=200, blank=True)
    cnpj_arrendataria = models.CharField(max_length=200, blank=True)
    sede_arrendataria = models.CharField(max_length=200, blank=True)
    municipio_arrendataria = models.CharField(max_length=200, blank=True)
    estado_arrendataria = models.CharField(max_length=200, blank=True)
    nome_representante_arrendataria = models.CharField(max_length=200, blank=True)
    qualificacao_representante = models.CharField(max_length=200, blank=True)
    endereco_comercial_representantes = models.CharField(max_length=200, blank=True)

    # Assinatura
    dia_assinatura = models.CharField(max_length=200, blank=True)
    mes_assinatura = models.CharField(max_length=200, blank=True)
    ano_assinatura = models.CharField(max_length=200, blank=True)

    # Reajuste e valores finais
    data_base_reajuste = models.CharField(max_length=200, blank=True)
    valor_parcela_outorga = models.CharField(max_length=200, blank=True)
    valor_parcela_outorga_extenso = models.CharField(max_length=200, blank=True)

    # Sedes institucionais
    sede_mpor = models.CharField(max_length=200, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_interno}"

class BlocoDaMinuta(models.Model):
    # blocos selecionados e que serão editados
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minuta = models.ForeignKey(MinutaGerada, on_delete=models.CASCADE, related_name='blocos')

    bloco_origem = models.ForeignKey(BlocoPadrao, on_delete=models.SET_NULL, blank=True, null=True, help_text="Referência ao bloco da biblioteca padrão que originou este.")

    # cópia do conteúdo do bloco padrão, para edição
    tipo = models.CharField(max_length=2, choices=TipoBloco.choices)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    conteudo_editado = RichTextField(blank=True, null=True)

    bloco_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_blocos')
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo or 'Sem título'}"
from django import forms

class MinutaEditalForm(forms.Form):
    leilao = forms.CharField(label="Número do Leilão", max_length=50, required=False)
    arrendamento = forms.CharField(label="Tipo de Arrendamento", max_length=200, required=False)
    perfil_da_carga = forms.CharField(label="Perfil da Carga", max_length=200, required=False)
    cargas_no_mme = forms.CharField(label="Cargas no MME", max_length=200, required=False)
    porto = forms.CharField(label="Porto Organizado", max_length=200, required=False)
    codigo_area = forms.CharField(label="Código da Área", max_length=100, required=False)
    poder_concedente = forms.CharField(label="Poder Concedente", max_length=200, required=False)
    data_publicacao_edital = forms.DateField(label="Data de Publicação do Edital", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_secao_recebimento_volume = forms.DateField(label="Data de Recebimento dos Volumes", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_secao_publica = forms.DateField(label="Data da Sessão Pública", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_publicacao_dou_audiencia = forms.DateField(label="Data de Publicação no DOU da Audiência", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_realizacao_audiencia = forms.DateField(label="Data de Realização da Audiência", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_consulta_publica = forms.CharField(label="Período da Consulta Pública", max_length=200, required=False)
    data_publicacao_dou_consulta_publica = forms.DateField(label="Data de Publicação no DOU da Consulta Pública", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    data_publicacao_edital_extenso = forms.CharField(label="Data do Edital por Extenso", max_length=200, required=False)
    # data no formato 'julho de 2024' para preencher o campo
    data_base = forms.CharField(label="Data Base para Preencher o Campo", max_length=200, required=False)
    # termo final do prazo para impugnação
    prazo_impugnacao = forms.CharField(label="Prazo para Impugnação", max_length=200, required=False)
    prazo_solicitacao_esclarecimento = forms.CharField(label="Prazo para Solicitação de Esclarecimento", max_length=200, required=False)
    # divulgação da decisão sobre eventual nã, Divulgação da decisão motivada da CPLA sobre eventual não aceitação dos documentos contidos no Volume 1 - Declarações Preliminares, Documentos de Representação e Garantia de Proposta - relativamente a cada um dos Arrendamentos objeto do Leilão.
    prazo_divulgacao_decisao_cpla = forms.CharField(label="Prazo para Divulgação da Decisão da CPLA", max_length=200, required=False)
    # publicacao da ata de julgamento relativa
    publicacao_ata_julgamento = forms.CharField(label="Data de Publicação da Ata de Julgamento", max_length=200, required=False)
    # abertura de brazo para interposição de recursos
    prazo_interposicao_recursos = forms.CharField(label="Prazo para Interposição de Recursos", max_length=200, required=False)
    resultado_interposicao_recursos = forms.CharField(label="Resultado da Interposição de Recursos", max_length=200, required=False)
    # data Divulgação, no sítio eletrônico do Ministério de Portos e AeroportosPoder Concedente e da ANTAQ, da ordem de classificação das propostas Propostas pelo Arrendamento. 
    data_divulgacao_classificacao_propostas = forms.CharField(label="Data de Divulgação da Classificação das Propostas", max_length=200, required=False)
    # data Divulgação, no sítio eletrônico do Ministério de Portos e AeroportosPoder Concedente e da ANTAQ, do resultado final do Leilão, após julgamento dos recursos eventualmente interpostos.
    data_divulgacao_resultado_final_leilao = forms.CharField(label="Data de Divulgação do Resultado Final do Leilão", max_length=200, required=False)

    modalidade_leilao = forms.CharField(label="Modalidade do Leilão", max_length=200, required=False)
    tipo_criterio = forms.CharField(label="Tipo de Critério de Julgamento", max_length=200, required=False)
    municipio = forms.CharField(label="Município do Porto", max_length=200, required=False)
    estado = forms.CharField(label="Estado do Porto", max_length=200, required=False)
    
    # dados sobre area do porto e prazo do arrendamento
    area_m2 = forms.CharField(label="Área em m² do Porto", max_length=200, required=False)
    area_m2_extenso = forms.CharField(label="Área do Porto por Extenso", max_length=200, required=False)
    prazo_arrendamento = forms.CharField(label="Prazo do Arrendamento", max_length=200, required=False)
    prazo_arrendamento_extenso = forms.CharField(label="Prazo do Arrendamento por Extenso", max_length=200, required=False)

    # visitas tecnicas a serem agendadas
    contato_visita_nome = forms.CharField(label="Nome do Contato para Visita Técnica", max_length=200, required=False)
    contato_visita_cargo = forms.CharField(label="Cargo do Contato para Visita Técnica", max_length=200, required=False)
    contato_visita_endereco = forms.CharField(label="Endereço do Contato para Visita Técnica", max_length=200, required=False)
    contato_visita_email = forms.EmailField(label="Email do Contato para Visita Técnica", required=False)

    # sobre garantia de proposta
    valor_garantia = forms.CharField(label="Valor da Garantia de Proposta", max_length=200, required=False)
    valor_garantia_extenso = forms.CharField(label="Valor da Garantia de Proposta por Extenso", max_length=200, required=False) 

    #remuneração b3
    remuneracao_b3 = forms.CharField(label="Remuneração da B3", max_length=200, required=False)
    remuneracao_b3_extenso = forms.CharField(label="Remuneração da B3 por Extenso", max_length=200, required=False)

    # remuneração à estruturadora
    remuneracao_estruturadora = forms.CharField(label="Remuneração da Estruturadora", max_length=200, required=False)
    remuneracao_estruturadora_extenso = forms.CharField(label="Remuneração da Estruturadora por Extenso", max_length=200, required=False)

    remuneracao_ap = forms.CharField(label="Remuneração da AP", max_length=200, required=False)
    remuneracao_ap_extenso = forms.CharField(label="Remuneração da AP por Extenso", max_length=200, required=False)

    # capital social
    valor_capital_social = forms.CharField(label="Valor do Capital Social", max_length=200, required=False)
    valor_capital_social_extenso = forms.CharField(label="Valor do Capital Social por Extenso", max_length=200, required=False)

    # periodo solicitação esclarecimento do edital
    inicio_esclarecimentos = forms.CharField(label="Início do Período de Solicitação de Esclarecimento do Edital", max_length=200, required=False)
    fim_esclarecimentos = forms.CharField(label="Fim do Período de Solicitação de Esclarecimento do Edital", max_length=200, required=False)

    # periodo solicitacao impugnacao do edital
    inicio_impugnacao = forms.CharField(label="Início do Período de Impugnação do Edital", max_length=200, required=False)
    fim_impugnacao = forms.CharField(label="Fim do Período de Impugnação do Edital", max_length=200, required=False)

    #divulgação ata impugnação do edital
    data_divulgacao_ata_impugnacao = forms.CharField(label="Data de Divulgação da Ata de Impugnação do Edital", max_length=200, required=False)


    #  check:
    # data_publicacao__dou_audiencia -> data_publicacao_dou_audiencia
    # perfil_da_carga
    # data_divulgacao_resultado_final_leilao
    # 


class MinutaContratoForm(forms.Form):
    leilao = forms.CharField(label="Número do Leilão", max_length=50, required=False)
    arrendamento = forms.CharField(label="Tipo de Arrendamento", max_length=200, required=False)
    perfil_da_carga = forms.CharField(label="Perfil da Carga", max_length=200, required=False)
    cargas_no_mme = forms.CharField(label="Cargas no MME", max_length=200, required=False)
    porto = forms.CharField(label="Porto Organizado", max_length=200, required=False)
    codigo_area = forms.CharField(label="Código da Área", max_length=100, required=False)
    poder_concedente = forms.CharField(label="Poder Concedente", max_length=200, required=False)

    numero_contrato = forms.CharField(label="Número do Contrato de Arrendamento", max_length=200, required=False)
    ano_contrato = forms.CharField(label="Ano do Contrato de Arrendamento", max_length=200, required=False)

    nome_secretario_portos = forms.CharField(label="Nome do Secretário de Portos", max_length=200, required=False)
    decreto_nomeacao_secretario = forms.CharField(label="Decreto de Nomeação do Secretário de Portos", max_length=200, required=False)
    data_decreto_secretario = forms.CharField(label="Data do Decreto de Nomeação do Secretário de Portos", max_length=200, required=False)

    nome_diretor_geral_antaq = forms.CharField(label="Nome do Diretor-Geral da ANTAQ", max_length=200, required=False)
    ato_designacao_diretor_antaq = forms.CharField(label="Ato de Designação do Diretor-Geral da ANTAQ", max_length=200, required=False)
    data_dou_diretor_antaq = forms.CharField(label="Data de Publicação no DOU do Diretor-Geral da ANTAQ", max_length=200, required=False)

    cnpj_autoridade_portuaria = forms.CharField(label="CNPJ da Autoridade Portuária", max_length=200, required=False)
    nome_diretor_presidente_ap = forms.CharField(label="Nome do Diretor-Presidente da Autoridade Portuária", max_length=200, required=False)
    ato_designacao_diretor_ap = forms.CharField(label="Ato de Designação do Diretor-Presidente da Autoridade Portuária", max_length=200, required=False)
    data_dou_diretor_ap = forms.CharField(label="Data de Publicação no DOU do Diretor-Presidente da Autoridade Portuária", max_length=200, required=False)

    nome_arrendataria = forms.CharField(label="Nome da Arrendatária", max_length=200, required=False)
    sede_arrendataria = forms.CharField(label="Sede da Arrendatária", max_length=200, required=False)
    cnpj_arrendataria = forms.CharField(label="CNPJ da Arrendatária", max_length=200, required=False)
    nome_representante_arrendataria = forms.CharField(label="Nome do Representante da Arrendatária", max_length=200, required=False)
    endereco_comercial_representantes = forms.CharField(label="Endereço Comercial dos Representantes da Arrendatária", max_length=200, required=False)
    numero_processo_administrativo = forms.CharField(label="Número do Processo Administrativo", max_length=200, required=False)

    numero_edital = forms.CharField(label="Número do Edital do Arrendamento", max_length=200, required=False)

    data_base_reajuste = forms.CharField(label="Data Base para Reajuste", max_length=200, required=False)
    data_base = forms.CharField(label="Data Base para Preencher o Campo", max_length=200, required=False)

    dia_assinatura = forms.CharField(label="Dia da Assinatura do Contrato", max_length=200, required=False)
    mes_assinatura = forms.CharField(label="Mês da Assinatura do Contrato", max_length=200, required=False)
    ano_assinatura = forms.CharField(label="Ano da Assinatura do Contrato", max_length=200, required=False)

    sede_mpor = forms.CharField(label="Sede do Ministério de Portos e Aeroportos", max_length=200, required=False)
    qualificacao_secretario_portos = forms.CharField(label="Qualificação do Secretário de Portos", max_length=200, required=False)
    data_dou_secretario = forms.CharField(label="Data de Publicação no DOU do Secretário de Portos", max_length=200, required=False)

    sede_antaq = forms.CharField(label="Sede da ANTAQ", max_length=200, required=False)
    qualificacao_diretor_geral_antaq = forms.CharField(label="Qualificação do Diretor-Geral da ANTAQ", max_length=200, required=False)
    nome_segundo_diretor = forms.CharField(label="Nome do Segundo Diretor da ANTAQ", max_length=200, required=False)
    ato_designacao_segundo_diretor = forms.CharField(label="Ato de Designação do Segundo Diretor da ANTAQ", max_length=200, required=False)
    data_dou_segundo_diretor = forms.CharField(label="Data de Publicação no DOU do Segundo Diretor da ANTAQ", max_length=200, required=False)

    sede_autoridade_portuaria = forms.CharField(label="Sede da Autoridade Portuária", max_length=200, required=False)
    qualificacao_diretor_presidente_ap = forms.CharField(label="Qualificação do Diretor-Presidente da Autoridade Portuária", max_length=200, required=False)
    
    municipio_arrendataria = forms.CharField(label="Município da Arrendatária", max_length=200, required=False)
    estado_arrendataria = forms.CharField(label="Estado da Arrendatária", max_length=200, required=False)

    tipo_sociedade_arrendataria = forms.CharField(label="Tipo de Sociedade da Arrendatária", max_length=200, required=False)
    qualificacao_representante = forms.CharField(label="Qualificação do Representante da Arrendatária", max_length=200, required=False)
    valor_parcela_outorga = forms.CharField(label="Valor da Parcela de Outorga", max_length=200, required=False)
    valor_parcela_outorga_extenso = forms.CharField(label="Valor da Parcela de Outorga por Extenso", max_length=200, required=False)


    # class MinutaEditalForm(forms.Form):

    # # INFORMAÇÕES GERAIS E DO OBJETO
    # leilao = forms.CharField(label="Número do Leilão", help_text="Ex: 01/2026", max_length=50, required=False)
    # arrendamento = forms.CharField(label="Objeto do Arrendamento", help_text="Ex: Arrendamento de Instalação Portuária", max_length=200, required=False)
    # perfil_da_carga = forms.CharField(label="Perfil da Carga", help_text="Ex: Granel Sólido Vegetal", max_length=200, required=False)
    # cargas_no_mme = forms.CharField(label="Tipos de Cargas Específicas", help_text="Detalhamento das cargas. Ex: Trigo, Milho e Soja.", max_length=200, required=False)
    # porto = forms.CharField(label="Nome do Porto Organizado", help_text="Ex: Porto de Santos", max_length=200, required=False)
    # codigo_area = forms.CharField(label="Código da Área (Terminal)", help_text="Ex: STS11", max_length=100, required=False)
    # poder_concedente = forms.CharField(label="Órgão do Poder Concedente", help_text="Ex: Ministério de Portos e Aeroportos", max_length=200, required=False)
    # municipio = forms.CharField(label="Município do Porto", help_text="Ex: Santos", max_length=200, required=False)
    # estado = forms.CharField(label="Estado (UF) do Porto", help_text="Ex: SP", max_length=200, required=False)
    
    # modalidade_leilao = forms.CharField(label="Modalidade da Licitação", help_text="Ex: Leilão", max_length=200, required=False)
    # tipo_criterio = forms.CharField(label="Critério de Julgamento", help_text="Ex: Maior Valor de Outorga", max_length=200, required=False)


    # # DADOS TÉCNICOS DA ÁREA E PRAZO
    # area_m2 = forms.CharField(label="Área Total (em m²)", help_text="Apenas números ou formato numérico. Ex: 621.975", max_length=200, required=False)
    # area_m2_extenso = forms.CharField(label="Área Total por Extenso", help_text="Ex: seiscentos e vinte e um mil e novecentos e setenta e cinco metros quadrados", max_length=200, required=False)
    # prazo_arrendamento = forms.CharField(label="Prazo do Arrendamento (em anos)", help_text="Ex: 25", max_length=200, required=False)
    # prazo_arrendamento_extenso = forms.CharField(label="Prazo do Arrendamento por Extenso", help_text="Ex: vinte e cinco anos", max_length=200, required=False)

    # # VALORES FINANCEIROS E GARANTIAS
    # data_base = forms.CharField(label="Data-Base para Reajuste Monetário", help_text="Mês e ano por extenso. Ex: julho de 2024", max_length=200, required=False)
    
    # valor_garantia = forms.CharField(label="Valor da Garantia de Proposta (R$)", help_text="Ex: 10.000.000,00", max_length=200, required=False)
    # valor_garantia_extenso = forms.CharField(label="Garantia da Proposta por Extenso", max_length=200, required=False) 

    # valor_capital_social = forms.CharField(label="Capital Social Mínimo Exigido (R$)", max_length=200, required=False)
    # valor_capital_social_extenso = forms.CharField(label="Capital Social Mínimo por Extenso", max_length=200, required=False)

    # remuneracao_b3 = forms.CharField(label="Valor de Remuneração da B3 (R$)", max_length=200, required=False)
    # remuneracao_b3_extenso = forms.CharField(label="Remuneração da B3 por Extenso", max_length=200, required=False)

    # remuneracao_estruturadora = forms.CharField(label="Valor de Remuneração da Estruturadora (R$)", help_text="Ex: EPL / Infra S.A.", max_length=200, required=False)
    # remuneracao_estruturadora_extenso = forms.CharField(label="Remuneração da Estruturadora por Extenso", max_length=200, required=False)

    # remuneracao_ap = forms.CharField(label="Valor de Remuneração da Autoridade Portuária (R$)", max_length=200, required=False)
    # remuneracao_ap_extenso = forms.CharField(label="Remuneração da AP por Extenso", max_length=200, required=False)

    # # CONTATOS PARA VISITA TÉCNICA
    # contato_visita_nome = forms.CharField(label="Visita Técnica: Nome do Contato", max_length=200, required=False)
    # contato_visita_cargo = forms.CharField(label="Visita Técnica: Cargo", max_length=200, required=False)
    # contato_visita_endereco = forms.CharField(label="Visita Técnica: Endereço", max_length=200, required=False)
    # contato_visita_email = forms.EmailField(label="Visita Técnica: E-mail", required=False)

    # # DATAS HISTÓRICAS (AUDIÊNCIA E CONSULTA)
    # data_publicacao_edital = forms.DateField(label="Data de Publicação do Edital", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    # data_publicacao_edital_extenso = forms.CharField(label="Data de Publicação do Edital por Extenso", help_text="Ex: 10 de maio de 2026", max_length=200, required=False)
    
    # data_publicacao_dou_audiencia = forms.DateField(label="Publicação no DOU (Aviso de Audiência Pública)", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    # data_realizacao_audiencia = forms.DateField(label="Data da Reunião de Audiência Pública", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    
    # data_publicacao_dou_consulta_publica = forms.DateField(label="Publicação no DOU (Aviso de Consulta Pública)", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    # data_consulta_publica = forms.CharField(label="Período da Consulta Pública", help_text="Ex: 15/01/2026 a 28/02/2026", max_length=200, required=False)

    # # CRONOGRAMA DO LEILÃO (EVENTOS FUTUROS)
    # data_secao_recebimento_volume = forms.DateField(label="Data da Sessão de Recebimento de Volumes (B3)", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    # data_secao_publica = forms.DateField(label="Data da Sessão Pública do Leilão (B3)", widget=forms.DateInput(attrs={"type": "date"}), required=False)
    
    # inicio_esclarecimentos = forms.CharField(label="Início do Prazo para Esclarecimentos", help_text="Ex: 10/03/2026", max_length=200, required=False)
    # fim_esclarecimentos = forms.CharField(label="Fim do Prazo para Esclarecimentos", max_length=200, required=False)
    # prazo_solicitacao_esclarecimento = forms.CharField(label="Data Limite para Resposta aos Esclarecimentos", max_length=200, required=False)

    # inicio_impugnacao = forms.CharField(label="Início do Prazo para Impugnação do Edital", max_length=200, required=False)
    # fim_impugnacao = forms.CharField(label="Fim do Prazo para Impugnação do Edital", max_length=200, required=False)
    # prazo_impugnacao = forms.CharField(label="Data Limite para Decisão sobre Impugnações", max_length=200, required=False)
    # data_divulgacao_ata_impugnacao = forms.CharField(label="Data de Publicação da Ata de Impugnação", max_length=200, required=False)

    # prazo_divulgacao_decisao_cpla = forms.CharField(label="Decisão da CPLA sobre Documentos (Volume 1)", help_text="Prazo para julgar as Declarações Preliminares.", max_length=200, required=False)
    # publicacao_ata_julgamento = forms.CharField(label="Publicação da Ata de Julgamento", max_length=200, required=False)
    
    # prazo_interposicao_recursos = forms.CharField(label="Período para Interposição de Recursos", help_text="Ex: 01/04/2026 a 05/04/2026", max_length=200, required=False)
    # resultado_interposicao_recursos = forms.CharField(label="Resultado dos Recursos (Julgamento)", max_length=200, required=False)
    
    # data_divulgacao_classificacao_propostas = forms.CharField(label="Divulgação da Classificação das Propostas", max_length=200, required=False)
    # data_divulgacao_resultado_final_leilao = forms.CharField(label="Homologação e Resultado Final do Leilão", max_length=200, required=False)
    # #  check:
    # # data_publicacao__dou_audiencia -> data_publicacao_dou_audiencia
    # # perfil_da_carga
    # # data_divulgacao_resultado_final_leilao
    # # 
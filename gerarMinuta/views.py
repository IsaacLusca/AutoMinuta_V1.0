import os

from django.shortcuts import render
from django.http import HttpResponse
from .forms import MinutaContratoForm, MinutaEditalForm
from docxtpl import DocxTemplate
from datetime import datetime
import io
from django.views.decorators.csrf import csrf_exempt
from pypdf import PdfReader
from google import genai
import json
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

CHAVE_API = os.getenv("CHAVE_API")
client = genai.Client(api_key=CHAVE_API)

def pagina_minutas(request):
    form_edital = MinutaEditalForm(prefix="edital")
    form_contrato = MinutaContratoForm(prefix="contrato")
    
    mensagem_ia = None
    tipo_mensagem = ""

    if request.method == "POST":

        if 'btn_analisar_ia' in request.POST:
            ficheiro_pdf = request.FILES.get('arquivo_pdf')
            
            if ficheiro_pdf:
                try:
                    # 1. Lê o PDF diretamente da memória RAM
                    leitor = PdfReader(ficheiro_pdf)
                    texto_completo = ""
                    for pagina in leitor.pages:
                        texto_pagina = pagina.extract_text()
                        if texto_pagina:
                            texto_completo += texto_pagina + "\n"

                    # 2. Envia apenas o texto para a IA (como fizemos no teste local)
                    prompt = """
                    Você é um assistente jurídico especialista em licitações portuárias da ANTAQ.
                    Analise os textos dos documentos fornecidos abaixo e extraia as seguintes informações. 
                    Se não encontrar a informação exata, deixe o valor em branco "".
                    
                    Responda ESTRITAMENTE em formato JSON, usando exatamente estas chaves:
                    {
                        "leilao": "Número do leilão (ex: 01/2026)",
                        "arrendamento": "Tipo de arrendamento (ex: Arrendamento portuário)",
                        "perfil_da_carga": "Perfil da carga (ex: Granéis sólidos vegetais)",
                        "cargas_no_mme": "Descrição das cargas no MME (ex: Soja e milho)",
                        "porto": "Nome do porto (ex: Porto de Santos)",
                        "codigo_area": "Código da área (ex: STS11)",
                        "poder_concedente": "Órgão concedente (ex: Ministério de Portos e Aeroportos)",
                        "data_publicacao_edital": "Data de publicação do edital (ex: 2026-03-10)",
                        "data_secao_recebimento_volume": "Data de recebimento dos volumes (ex: 2026-04-15)",
                        "data_secao_publica": "Data da sessão pública (ex: 2026-04-20)",
                        "data_publicacao_dou_audiencia": "Data de publicação no DOU da audiência (ex: 2026-02-01)",
                        "data_realizacao_audiencia": "Data de realização da audiência (ex: 2026-02-15)",
                        "data_consulta_publica": "Período da consulta pública (ex: 10/01/2026 a 10/02/2026)",
                        "data_publicacao_dou_consulta_publica": "Data de publicação no DOU da consulta pública (ex: 2026-01-09)",
                        "data_publicacao_edital_extenso": "Data do edital por extenso (ex: 10 de março de 2026)",
                        "data_base": "Data base por extenso (ex: março de 2026)",
                        "prazo_impugnacao": "Prazo final para impugnação (ex: 05 dias úteis após publicação)",
                        "prazo_solicitacao_esclarecimento": "Prazo para solicitação de esclarecimento (ex: até 5 dias úteis antes da sessão)",
                        "prazo_divulgacao_decisao_cpla": "Prazo para divulgação da decisão da CPLA (ex: até 3 dias úteis após análise)",
                        "publicacao_ata_julgamento": "Data de publicação da ata de julgamento (ex: 2026-04-25)",
                        "prazo_interposicao_recursos": "Prazo para interposição de recursos (ex: 5 dias úteis)",
                        "resultado_interposicao_recursos": "Data ou descrição do resultado dos recursos (ex: 2026-05-05)",
                        "data_divulgacao_classificacao_propostas": "Data de divulgação da classificação das propostas (ex: 2026-05-01)",
                        "data_divulgacao_resultado_final_leilao": "Data de divulgação do resultado final do leilão (ex: 2026-05-10)",
                        "modalidade_leilao": "Modalidade do leilão (ex: Leilão eletrônico)",
                        "tipo_criterio": "Critério de julgamento (ex: Maior valor de outorga)",
                        "municipio": "Município do porto (ex: Santos)",
                        "estado": "Estado do porto (ex: SP)",
                        "area_m2": "Área em m² (ex: 100000)",
                        "area_m2_extenso": "Área por extenso (ex: cem mil metros quadrados)",
                        "prazo_arrendamento": "Prazo em anos (ex: 25)",
                        "prazo_arrendamento_extenso": "Prazo por extenso (ex: vinte e cinco anos)",
                        "contato_visita_nome": "Nome do contato para visita técnica (ex: João Silva)",
                        "contato_visita_cargo": "Cargo do contato (ex: Gerente de Operações)",
                        "contato_visita_endereco": "Endereço para visita técnica (ex: Av. Portuária, 1000, Santos/SP)",
                        "contato_visita_email": "Email para agendamento de visita (ex: visitas@porto.gov.br)",
                        "valor_garantia": "Valor da garantia em números (ex: 15.000.000,00)",
                        "valor_garantia_extenso": "Valor da garantia por extenso (ex: quinze milhões de reais)",
                        "remuneracao_b3": "Valor da remuneração da B3 em números (ex: 500.000,00)",
                        "remuneracao_b3_extenso": "Valor da remuneração da B3 por extenso (ex: quinhentos mil reais)",
                        "remuneracao_estruturadora": "Valor da remuneração da estruturadora em números (ex: 300.000,00)",
                        "remuneracao_estruturadora_extenso": "Valor da remuneração da estruturadora por extenso (ex: trezentos mil reais)",
                        "remuneracao_ap": "Valor da remuneração da AP em números (ex: 200.000,00)",
                        "remuneracao_ap_extenso": "Valor da remuneração da AP por extenso (ex: duzentos mil reais)",
                        "valor_capital_social": "Valor do capital social em números (ex: 50.000.000,00)",
                        "valor_capital_social_extenso": "Valor do capital social por extenso (ex: cinquenta milhões de reais)",
                        "inicio_esclarecimentos": "Data de início dos esclarecimentos (ex: 2026-03-01)",
                        "fim_esclarecimentos": "Data de fim dos esclarecimentos (ex: 2026-03-20)",
                        "inicio_impugnacao": "Data de início da impugnação (ex: 2026-03-01)",
                        "fim_impugnacao": "Data de fim da impugnação (ex: 2026-03-10)",
                        "data_divulgacao_ata_impugnacao": "Data de divulgação da ata de impugnação (ex: 2026-03-15)",
                        "numero_contrato": "Número do contrato de arrendamento (ex: 001)",
                        "ano_contrato": "Ano do contrato de arrendamento (ex: 2026)",
                        "nome_secretario_portos": "Nome do secretário de portos (ex: João Silva)",
                        "decreto_nomeacao_secretario": "Decreto de nomeação do secretário de portos (ex: 123/2025)",
                        "data_decreto_secretario": "Data do decreto de nomeação do secretário de portos (ex: 2025-01-15)",
                        "nome_diretor_geral_antaq": "Nome do diretor-geral da ANTAQ (ex: Maria Santos)",
                        "ato_designacao_diretor_antaq": "Ato de designação do diretor-geral da ANTAQ (ex: 456/2025)",
                        "data_dou_diretor_antaq": "Data de publicação no DOU do diretor-geral da ANTAQ (ex: 2025-01-20)",
                        "cnpj_autoridade_portuaria": "CNPJ da autoridade portuária (ex: 12.345.678/0001-90)",
                        "nome_diretor_presidente_ap": "Nome do diretor-presidente da autoridade portuária (ex: Pedro Oliveira)",
                        "ato_designacao_diretor_ap": "Ato de designação do diretor-presidente da autoridade portuária (ex: 789/2025)",
                        "data_dou_diretor_ap": "Data de publicação no DOU do diretor-presidente da autoridade portuária (ex: 2025-01-25)",
                        "nome_arrendataria": "Nome da arrendatária (ex: ABC Logística S/A)",
                        "sede_arrendataria": "Sede da arrendatária (ex: Rua Principal, 100)",
                        "cnpj_arrendataria": "CNPJ da arrendatária (ex: 98.765.432/0001-10)",
                        "nome_representante_arrendataria": "Nome do representante da arrendatária (ex: Carlos Costa)",
                        "endereco_comercial_representantes": "Endereço comercial dos representantes da arrendatária (ex: Av. Secundária, 200)",
                        "numero_processo_administrativo": "Número do processo administrativo (ex: 2025.001.234)",
                        "numero_edital": "Número do edital do arrendamento (ex: 01/2025)",
                        "data_base_reajuste": "Data base para reajuste (ex: 2026-03-10)",
                        "dia_assinatura": "Dia da assinatura do contrato (ex: 15)",
                        "mes_assinatura": "Mês da assinatura do contrato (ex: 03)",
                        "ano_assinatura": "Ano da assinatura do contrato (ex: 2026)",
                        "sede_mpor": "Sede do Ministério de Portos e Aeroportos (ex: Brasília/DF)",
                        "qualificacao_secretario_portos": "Qualificação do secretário de portos (ex: Decreto nº 123/2025, DOU 15/01/2025)",
                        "data_dou_secretario": "Data de publicação no DOU do secretário de portos (ex: 2025-01-15)",
                        "sede_antaq": "Sede da ANTAQ (ex: Brasília/DF)",
                        "qualificacao_diretor_geral_antaq": "Qualificação do diretor-geral da ANTAQ (ex: Ato nº 456/2025, DOU 20/01/2025)",
                        "nome_segundo_diretor": "Nome do segundo diretor da ANTAQ (ex: Ana Silva)",
                        "ato_designacao_segundo_diretor": "Ato de designação do segundo diretor da ANTAQ (ex: 457/2025)",
                        "data_dou_segundo_diretor": "Data de publicação no DOU do segundo diretor da ANTAQ (ex: 2025-01-21)",
                        "sede_autoridade_portuaria": "Sede da autoridade portuária (ex: Santos/SP)",
                        "qualificacao_diretor_presidente_ap": "Qualificação do diretor-presidente da autoridade portuária (ex: Ato nº 789/2025, DOU 25/01/2025)",
                        "municipio_arrendataria": "Município da arrendatária (ex: Santos)",
                        "estado_arrendataria": "Estado da arrendatária (ex: SP)",
                        "tipo_sociedade_arrendataria": "Tipo de sociedade da arrendatária (ex: Sociedade Anônima)",
                        "qualificacao_representante": "Qualificação do representante da arrendatária (ex: CPF 123.456.789-00)",
                        "valor_parcela_outorga": "Valor da parcela de outorga (ex: 1.000.000,00)",
                        "valor_parcela_outorga_extenso": "Valor da parcela de outorga por extenso (ex: um milhão de reais)"
                    }
                    Não inclua nenhum texto adicional antes ou depois do JSON.
                    
                    TEXTO DOS DOCUMENTOS:
                    """ + texto_completo

                    resposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    # 3. Limpa e converte o resultado para Dicionário
                    texto_limpo = resposta.text.replace('```json', '').replace('```', '').strip()
                    dados_extraidos = json.loads(texto_limpo)
                    
                    form_edital = MinutaEditalForm(initial=dados_extraidos, prefix="edital")
                    form_contrato = MinutaContratoForm(initial=dados_extraidos, prefix="contrato")
                    mensagem_ia = "Campos preenchidos com sucesso!"
                    tipo_mensagem = "success"
                    
                except Exception as e:
                    mensagem_ia = f"Erro na IA: {str(e)}"
                    tipo_mensagem = "danger"
            else:
                mensagem_ia = "Selecione um PDF antes de analisar."
                tipo_mensagem = "warning"

        elif 'btn_gerar_edital' in request.POST:
            form_edital = MinutaEditalForm(request.POST, prefix="edital")
            if form_edital.is_valid():
                dados = form_edital.cleaned_data
                doc = DocxTemplate("testes/MINUTA DE EDITAL.docx")
                contexto = {
                    "leilao": dados["leilao"],
                    "arrendamento": dados["arrendamento"],
                    "perfil_da_carga": dados["perfil_da_carga"],
                    "cargas_no_mme": dados["cargas_no_mme"],
                    "porto": dados["porto"],
                    "codigo_area": dados["codigo_area"],
                    "poder_concedente": dados["poder_concedente"],
                    "data_publicacao_edital": dados["data_publicacao_edital"].strftime("%d/%m/%Y") if dados["data_publicacao_edital"] else "[•] [•] [•]",
                    "data_secao_recebimento_volume": dados["data_secao_recebimento_volume"].strftime("%d/%m/%Y") if dados["data_secao_recebimento_volume"] else "[•] [•] [•]",
                    "data_secao_publica": dados["data_secao_publica"].strftime("%d/%m/%Y") if dados["data_secao_publica"] else "[•] [•] [•]",
                    "data_publicacao_dou_audiencia": dados["data_publicacao_dou_audiencia"].strftime("%d/%m/%Y") if dados["data_publicacao_dou_audiencia"] else "[•] [•] [•]",
                    "data_realizacao_audiencia": dados["data_realizacao_audiencia"].strftime("%d/%m/%Y") if dados["data_realizacao_audiencia"] else "[•] [•] [•]",
                    "data_consulta_publica": dados["data_consulta_publica"],
                    "data_publicacao_dou_consulta_publica": dados["data_publicacao_dou_consulta_publica"].strftime("%d/%m/%Y") if dados["data_publicacao_dou_consulta_publica"] else "[•] [•] [•]",
                    "data_publicacao_edital_extenso": dados["data_publicacao_edital_extenso"],
                    "data_base": dados["data_base"],
                    "prazo_impugnacao": dados["prazo_impugnacao"],
                    "prazo_solicitacao_esclarecimento": dados["prazo_solicitacao_esclarecimento"],
                    "prazo_divulgacao_decisao_cpla": dados["prazo_divulgacao_decisao_cpla"],
                    "publicacao_ata_julgamento": dados["publicacao_ata_julgamento"],
                    "prazo_interposicao_recursos": dados["prazo_interposicao_recursos"],
                    "resultado_interposicao_recursos": dados["resultado_interposicao_recursos"],
                    "data_divulgacao_classificacao_propostas": dados["data_divulgacao_classificacao_propostas"],
                    "data_divulgacao_resultado_final_leilao": dados["data_divulgacao_resultado_final_leilao"],
                    # Novos campos adicionados à classe MinutaEdital
                    "modalidade_leilao": dados["modalidade_leilao"],
                    "tipo_criterio": dados["tipo_criterio"],
                    "municipio": dados["municipio"],
                    "estado": dados["estado"],

                    # dados sobre area do porto e prazo do arrendamento
                    "area_m2": dados["area_m2"],
                    "area_m2_extenso": dados["area_m2_extenso"],
                    "prazo_arrendamento": dados["prazo_arrendamento"],
                    "prazo_arrendamento_extenso": dados["prazo_arrendamento_extenso"],

                    # visitas tecnicas a serem agendadas
                    "contato_visita_nome": dados["contato_visita_nome"],
                    "contato_visita_cargo": dados["contato_visita_cargo"],
                    "contato_visita_endereco": dados["contato_visita_endereco"],
                    "contato_visita_email": dados["contato_visita_email"],

                    # sobre garantia de proposta
                    "valor_garantia": dados["valor_garantia"],
                    "valor_garantia_extenso": dados["valor_garantia_extenso"],

                    # remuneracao b3
                    "remuneracao_b3": dados["remuneracao_b3"],
                    "remuneracao_b3_extenso": dados["remuneracao_b3_extenso"],

                    # remuneracao à estruturadora
                    "remuneracao_estruturadora": dados["remuneracao_estruturadora"],
                    "remuneracao_estruturadora_extenso": dados["remuneracao_estruturadora_extenso"],

                    "remuneracao_ap": dados["remuneracao_ap"],
                    "remuneracao_ap_extenso": dados["remuneracao_ap_extenso"],

                    # capital social
                    "valor_capital_social": dados["valor_capital_social"],
                    "valor_capital_social_extenso": dados["valor_capital_social_extenso"],

                    # periodo solicitação esclarecimento do edital
                    "inicio_esclarecimentos": dados["inicio_esclarecimentos"],
                    "fim_esclarecimentos": dados["fim_esclarecimentos"],

                    # periodo solicitacao impugnacao do edital
                    "inicio_impugnacao": dados["inicio_impugnacao"],
                    "fim_impugnacao": dados["fim_impugnacao"],

                    # divulgação ata impugnação do edital
                    "data_divulgacao_ata_impugnacao": dados["data_divulgacao_ata_impugnacao"],
                }

                doc.render(contexto)
                # arquivo temp na ram para otimizar o processo de download
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                response = HttpResponse(
                    buffer.read(),
                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                response["Content-Disposition"] = "attachment; filename=resultado_formulario.docx"
                return response

        elif 'btn_gerar_contrato' in request.POST:
            form_contrato = MinutaContratoForm(request.POST, prefix="contrato")
            if form_contrato.is_valid():
                dados = form_contrato.cleaned_data
                doc = DocxTemplate("testes/MINUTA DE CONTRATO.docx")

                contexto = {
                    "leilao": dados["leilao"],
                    "arrendamento": dados["arrendamento"],
                    "perfil_da_carga": dados["perfil_da_carga"],
                    "cargas_no_mme": dados["cargas_no_mme"],
                    "porto": dados["porto"],
                    "codigo_area": dados["codigo_area"],
                    "poder_concedente": dados["poder_concedente"],

                    "numero_contrato": dados["numero_contrato"],
                    "ano_contrato": dados["ano_contrato"],

                    "nome_secretario_portos": dados["nome_secretario_portos"],
                    "decreto_nomeacao_secretario": dados["decreto_nomeacao_secretario"],
                    "data_decreto_secretario": dados["data_decreto_secretario"],

                    "nome_diretor_geral_antaq": dados["nome_diretor_geral_antaq"],
                    "ato_designacao_diretor_antaq": dados["ato_designacao_diretor_antaq"],
                    "data_dou_diretor_antaq": dados["data_dou_diretor_antaq"],

                    "cnpj_autoridade_portuaria": dados["cnpj_autoridade_portuaria"],
                    "nome_diretor_presidente_ap": dados["nome_diretor_presidente_ap"],
                    "ato_designacao_diretor_ap": dados["ato_designacao_diretor_ap"],
                    "data_dou_diretor_ap": dados["data_dou_diretor_ap"],

                    "nome_arrendataria": dados["nome_arrendataria"],
                    "sede_arrendataria": dados["sede_arrendataria"],
                    "cnpj_arrendataria": dados["cnpj_arrendataria"],
                    "nome_representante_arrendataria": dados["nome_representante_arrendataria"],
                    "endereco_comercial_representantes": dados["endereco_comercial_representantes"],
                    "numero_processo_administrativo": dados["numero_processo_administrativo"],

                    "numero_edital": dados["numero_edital"],

                    "data_base_reajuste": dados["data_base_reajuste"],
                    "data_base": dados["data_base"],

                    "dia_assinatura": dados["dia_assinatura"],
                    "mes_assinatura": dados["mes_assinatura"],
                    "ano_assinatura": dados["ano_assinatura"],

                    "sede_mpor": dados["sede_mpor"],
                    "qualificacao_secretario_portos": dados["qualificacao_secretario_portos"],
                    "data_dou_secretario": dados["data_dou_secretario"],

                    "sede_antaq": dados["sede_antaq"],
                    "qualificacao_diretor_geral_antaq": dados["qualificacao_diretor_geral_antaq"],
                    "nome_segundo_diretor": dados["nome_segundo_diretor"],
                    "ato_designacao_segundo_diretor": dados["ato_designacao_segundo_diretor"],
                    "data_dou_segundo_diretor": dados["data_dou_segundo_diretor"],

                    "sede_autoridade_portuaria": dados["sede_autoridade_portuaria"],
                    "qualificacao_diretor_presidente_ap": dados["qualificacao_diretor_presidente_ap"],

                    "municipio_arrendataria": dados["municipio_arrendataria"],
                    "estado_arrendataria": dados["estado_arrendataria"],

                    "tipo_sociedade_arrendataria": dados["tipo_sociedade_arrendataria"],
                    "qualificacao_representante": dados["qualificacao_representante"],
                    "valor_parcela_outorga": dados["valor_parcela_outorga"],
                    "valor_parcela_outorga_extenso": dados["valor_parcela_outorga_extenso"],
                    }
                
                doc.render(contexto)
                # arquivo temp na ram para otimizar o processo de download
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                response = HttpResponse(
                    buffer.read(),
                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                response["Content-Disposition"] = "attachment; filename=resultado_formulario.docx"
                return response
            
    return render(request, "form.html", {
        "form_edital": form_edital,
        "form_contrato": form_contrato,
        "mensagem_ia": mensagem_ia,
        "tipo_mensagem": tipo_mensagem
    })



# from django.shortcuts import render
# from django.http import HttpResponse
# from .forms import MinutaContratoForm, MinutaEditalForm
# from docxtpl import DocxTemplate
# from datetime import datetime
# import io

# def pagina_minutas(request):
#     form_edital = MinutaEditalForm(prefix="edital")
#     form_contrato = MinutaContratoForm(prefix="contrato")

#     if request.method == "POST":

#         if 'btn_gerar_edital' in request.POST:
#             form_edital = MinutaEditalForm(request.POST, prefix="edital")
#             if form_edital.is_valid():
#                 dados = form_edital.cleaned_data
#                 doc = DocxTemplate("testes/MINUTA DE EDITAL.docx")
#                 contexto = {
#                     "leilao": dados["leilao"],
#                     "arrendamento": dados["arrendamento"],
#                     "perfil_da_carga": dados["perfil_da_carga"],
#                     "cargas_no_mme": dados["cargas_no_mme"],
#                     "porto": dados["porto"],
#                     "codigo_area": dados["codigo_area"],
#                     "poder_concedente": dados["poder_concedente"],
#                     "data_publicacao_edital": dados["data_publicacao_edital"].strftime("%d/%m/%Y") if dados["data_publicacao_edital"] else "[•] [•] [•]",
#                     "data_secao_recebimento_volume": dados["data_secao_recebimento_volume"].strftime("%d/%m/%Y") if dados["data_secao_recebimento_volume"] else "[•] [•] [•]",
#                     "data_secao_publica": dados["data_secao_publica"].strftime("%d/%m/%Y") if dados["data_secao_publica"] else "[•] [•] [•]",
#                     "data_publicacao_dou_audiencia": dados["data_publicacao_dou_audiencia"].strftime("%d/%m/%Y") if dados["data_publicacao_dou_audiencia"] else "[•] [•] [•]",
#                     "data_realizacao_audiencia": dados["data_realizacao_audiencia"].strftime("%d/%m/%Y") if dados["data_realizacao_audiencia"] else "[•] [•] [•]",
#                     "data_consulta_publica": dados["data_consulta_publica"],
#                     "data_publicacao_dou_consulta_publica": dados["data_publicacao_dou_consulta_publica"].strftime("%d/%m/%Y") if dados["data_publicacao_dou_consulta_publica"] else "[•] [•] [•]",
#                     "data_publicacao_edital_extenso": dados["data_publicacao_edital_extenso"],
#                     "data_base": dados["data_base"],
#                     "prazo_impugnacao": dados["prazo_impugnacao"],
#                     "prazo_solicitacao_esclarecimento": dados["prazo_solicitacao_esclarecimento"],
#                     "prazo_divulgacao_decisao_cpla": dados["prazo_divulgacao_decisao_cpla"],
#                     "publicacao_ata_julgamento": dados["publicacao_ata_julgamento"],
#                     "prazo_interposicao_recursos": dados["prazo_interposicao_recursos"],
#                     "resultado_interposicao_recursos": dados["resultado_interposicao_recursos"],
#                     "data_divulgacao_classificacao_propostas": dados["data_divulgacao_classificacao_propostas"],
#                     "data_divulgacao_resultado_final_leilao": dados["data_divulgacao_resultado_final_leilao"],
#                     # Novos campos adicionados à classe MinutaEdital
#                     "modalidade_leilao": dados["modalidade_leilao"],
#                     "tipo_criterio": dados["tipo_criterio"],
#                     "municipio": dados["municipio"],
#                     "estado": dados["estado"],

#                     # dados sobre area do porto e prazo do arrendamento
#                     "area_m2": dados["area_m2"],
#                     "area_m2_extenso": dados["area_m2_extenso"],
#                     "prazo_arrendamento": dados["prazo_arrendamento"],
#                     "prazo_arrendamento_extenso": dados["prazo_arrendamento_extenso"],

#                     # visitas tecnicas a serem agendadas
#                     "contato_visita_nome": dados["contato_visita_nome"],
#                     "contato_visita_cargo": dados["contato_visita_cargo"],
#                     "contato_visita_endereco": dados["contato_visita_endereco"],
#                     "contato_visita_email": dados["contato_visita_email"],

#                     # sobre garantia de proposta
#                     "valor_garantia": dados["valor_garantia"],
#                     "valor_garantia_extenso": dados["valor_garantia_extenso"],

#                     # remuneracao b3
#                     "remuneracao_b3": dados["remuneracao_b3"],
#                     "remuneracao_b3_extenso": dados["remuneracao_b3_extenso"],

#                     # remuneracao à estruturadora
#                     "remuneracao_estruturadora": dados["remuneracao_estruturadora"],
#                     "remuneracao_estruturadora_extenso": dados["remuneracao_estruturadora_extenso"],

#                     "remuneracao_ap": dados["remuneracao_ap"],
#                     "remuneracao_ap_extenso": dados["remuneracao_ap_extenso"],

#                     # capital social
#                     "valor_capital_social": dados["valor_capital_social"],
#                     "valor_capital_social_extenso": dados["valor_capital_social_extenso"],

#                     # periodo solicitação esclarecimento do edital
#                     "inicio_esclarecimentos": dados["inicio_esclarecimentos"],
#                     "fim_esclarecimentos": dados["fim_esclarecimentos"],

#                     # periodo solicitacao impugnacao do edital
#                     "inicio_impugnacao": dados["inicio_impugnacao"],
#                     "fim_impugnacao": dados["fim_impugnacao"],

#                     # divulgação ata impugnação do edital
#                     "data_divulgacao_ata_impugnacao": dados["data_divulgacao_ata_impugnacao"],
#                 }

#                 doc.render(contexto)
#                 # arquivo temp na ram para otimizar o processo de download
#                 buffer = io.BytesIO()
#                 doc.save(buffer)
#                 buffer.seek(0)
#                 response = HttpResponse(
#                     buffer.read(),
#                     content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                 )
#                 response["Content-Disposition"] = "attachment; filename=resultado_formulario.docx"
#                 return response

#         elif 'btn_gerar_contrato' in request.POST:
#             form_contrato = MinutaContratoForm(request.POST, prefix="contrato")
#             if form_contrato.is_valid():
#                 dados = form_contrato.cleaned_data
#                 doc = DocxTemplate("testes/MINUTA DE CONTRATO.docx")

#                 contexto = {
#                     "leilao": dados["leilao"],
#                     "arrendamento": dados["arrendamento"],
#                     "perfil_da_carga": dados["perfil_da_carga"],
#                     "cargas_no_mme": dados["cargas_no_mme"],
#                     "porto": dados["porto"],
#                     "codigo_area": dados["codigo_area"],
#                     "poder_concedente": dados["poder_concedente"],

#                     "numero_contrato": dados["numero_contrato"],
#                     "ano_contrato": dados["ano_contrato"],

#                     "nome_secretario_portos": dados["nome_secretario_portos"],
#                     "decreto_nomeacao_secretario": dados["decreto_nomeacao_secretario"],
#                     "data_decreto_secretario": dados["data_decreto_secretario"],

#                     "nome_diretor_geral_antaq": dados["nome_diretor_geral_antaq"],
#                     "ato_designacao_diretor_antaq": dados["ato_designacao_diretor_antaq"],
#                     "data_dou_diretor_antaq": dados["data_dou_diretor_antaq"],

#                     "cnpj_autoridade_portuaria": dados["cnpj_autoridade_portuaria"],
#                     "nome_diretor_presidente_ap": dados["nome_diretor_presidente_ap"],
#                     "ato_designacao_diretor_ap": dados["ato_designacao_diretor_ap"],
#                     "data_dou_diretor_ap": dados["data_dou_diretor_ap"],

#                     "nome_arrendataria": dados["nome_arrendataria"],
#                     "sede_arrendataria": dados["sede_arrendataria"],
#                     "cnpj_arrendataria": dados["cnpj_arrendataria"],
#                     "nome_representante_arrendataria": dados["nome_representante_arrendataria"],
#                     "endereco_comercial_representantes": dados["endereco_comercial_representantes"],
#                     "numero_processo_administrativo": dados["numero_processo_administrativo"],

#                     "numero_edital": dados["numero_edital"],

#                     "data_base_reajuste": dados["data_base_reajuste"],
#                     "data_base": dados["data_base"],

#                     "dia_assinatura": dados["dia_assinatura"],
#                     "mes_assinatura": dados["mes_assinatura"],
#                     "ano_assinatura": dados["ano_assinatura"],

#                     "sede_mpor": dados["sede_mpor"],
#                     "qualificacao_secretario_portos": dados["qualificacao_secretario_portos"],
#                     "data_dou_secretario": dados["data_dou_secretario"],

#                     "sede_antaq": dados["sede_antaq"],
#                     "qualificacao_diretor_geral_antaq": dados["qualificacao_diretor_geral_antaq"],
#                     "nome_segundo_diretor": dados["nome_segundo_diretor"],
#                     "ato_designacao_segundo_diretor": dados["ato_designacao_segundo_diretor"],
#                     "data_dou_segundo_diretor": dados["data_dou_segundo_diretor"],

#                     "sede_autoridade_portuaria": dados["sede_autoridade_portuaria"],
#                     "qualificacao_diretor_presidente_ap": dados["qualificacao_diretor_presidente_ap"],

#                     "municipio_arrendataria": dados["municipio_arrendataria"],
#                     "estado_arrendataria": dados["estado_arrendataria"],

#                     "tipo_sociedade_arrendataria": dados["tipo_sociedade_arrendataria"],
#                     "qualificacao_representante": dados["qualificacao_representante"],
#                     "valor_parcela_outorga": dados["valor_parcela_outorga"],
#                     "valor_parcela_outorga_extenso": dados["valor_parcela_outorga_extenso"],
#                     }
                
#                 doc.render(contexto)
#                 # arquivo temp na ram para otimizar o processo de download
#                 buffer = io.BytesIO()
#                 doc.save(buffer)
#                 buffer.seek(0)
#                 response = HttpResponse(
#                     buffer.read(),
#                     content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                 )
#                 response["Content-Disposition"] = "attachment; filename=resultado_formulario.docx"
#                 return response
            
#     return render(request, "form.html", {
#         "form_edital": form_edital,
#         "form_contrato": form_contrato
#     })
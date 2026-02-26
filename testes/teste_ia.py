from google import genai
from pypdf import PdfReader
import json

# 1. Configuração do Cliente
CHAVE_API = ""
client = genai.Client(api_key=CHAVE_API)

def extrair_texto_localmente(lista_caminhos_pdf):
    texto_acumulado = ""
    print(f"Lendo {len(lista_caminhos_pdf)} arquivos localmente...")
    
    for caminho in lista_caminhos_pdf:
        try:
            print(f"  - Extraindo texto de: {caminho}")
            leitor = PdfReader(caminho)
            
            texto_acumulado += f"\n\n--- INÍCIO DO DOCUMENTO: {caminho} ---\n"
            
            # Extrai o texto página por página
            for pagina in leitor.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_acumulado += texto_pagina + "\n"
                    
            texto_acumulado += f"\n--- FIM DO DOCUMENTO: {caminho} ---\n"
        except Exception as e:
            print(f"  ⚠️ Erro ao ler {caminho}: {e}")
            
    return texto_acumulado

def analisar_textos_com_ia(texto_completo):
    print("\nEnviando o texto extraído para a IA processar (isso economiza muitos tokens!)...")
    
    prompt = """
    Você é um assistente jurídico especialista em licitações portuárias da ANTAQ.
    Analise os textos dos documentos fornecidos abaixo e extraia as seguintes informações. 
    Se não encontrar a informação exata, deixe o valor em branco "".
    
    Responda ESTRITAMENTE em formato JSON, usando exatamente estas chaves:
    {
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
        "data_divulgacao_ata_impugnacao": "Data de divulgação da ata de impugnação (ex: 2026-03-15)"
        }
    }
    Não inclua nenhum texto adicional antes ou depois do JSON.
    
    TEXTO DOS DOCUMENTOS:
    """ + texto_completo

    try:
        # Chama a IA enviando apenas o texto puro
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        texto_limpo = resposta.text.replace('```json', '').replace('```', '').strip()
        dados_extraidos = json.loads(texto_limpo)
        
        print("\n✅ SUCESSO! Dados extraídos:")
        print(json.dumps(dados_extraidos, indent=4, ensure_ascii=False))
        return dados_extraidos
        
    except Exception as e:
        print(f"\n❌ Erro durante a extração: {e}")

if __name__ == "__main__":
    # Agora você pode colocar a lista com os 11 arquivos!
    meus_documentos = [
        'testes/nota-tecnica.pdf',
    ]
    
    # Passo A: O seu PC faz o trabalho pesado de ler o PDF
    texto_dos_pdfs = extrair_texto_localmente(meus_documentos)
    
    # Passo B: A IA só faz o trabalho inteligente de achar os dados
    if texto_dos_pdfs.strip():
        analisar_textos_com_ia(texto_dos_pdfs)
    else:
        print("Nenhum texto foi encontrado nos PDFs (eles podem ser imagens escaneadas).")
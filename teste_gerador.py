from docxtpl import DocxTemplate
import os

def gerar_minuta_teste():
    # Caminho do arquivo de template (ajuste conforme o nome real do seu arquivo)
    template_path = "testes/MINUTA DE EDITAL.docx" 
    output_path = "resultado_teste_edital.docx"

    print(f"Carregando o template: {template_path}...")
    
    if not os.path.exists(template_path):
        print(f"ERRO: Arquivo '{template_path}' não encontrado!")
        print("Certifique-se de que o caminho está correto.")
        return

    doc = DocxTemplate(template_path)

    # Dicionário simulando o 'form.cleaned_data' vindo do Django
    dados_teste = {
        "leilao": "01/2026",
        "arrendamento": "Arrendamento de Instalação Portuária",
        "perfil_da_carga": "Granel Sólido Vegetal",
        "cargas_no_mme": "Milho e Soja",
        "porto": "Porto de Santos",
        "codigo_area": "STS11",
        "poder_concedente": "Ministério de Portos e Aeroportos",
        
        # Cronograma e Datas (tudo como texto livre agora)
        "data_publicacao_edital": "25/02/2026",
        "data_secao_recebimento_volume": "10/04/2026",
        "data_secao_publica": "15/04/2026",
        "data_publicacao_dou_audiencia": "10/01/2026",
        "data_realizacao_audiencia": "20/01/2026",
        "data_consulta_publica": "01/01/2026 a 15/02/2026",
        "data_publicacao_dou_consulta_publica": "01/01/2026",
        "data_publicacao_edital_extenso": "vinte e cinco de fevereiro de dois mil e vinte e seis",
        "data_base": "fevereiro de 2026",
        "prazo_impugnacao": "05/03/2026",
        "prazo_solicitacao_esclarecimento": "01/03/2026",
        "prazo_divulgacao_decisao_cpla": "12/04/2026",
        "publicacao_ata_julgamento": "20/04/2026",
        "prazo_interposicao_recursos": "25/04/2026",
        "resultado_interposicao_recursos": "05/05/2026",
        "data_divulgacao_classificacao_propostas": "16/04/2026",
        "data_divulgacao_resultado_final_leilao": "10/05/2026",
        
        # Características da Área
        "modalidade_leilao": "Leilão",
        "tipo_criterio": "Maior Valor de Outorga",
        "municipio": "Santos",
        "estado": "SP",
        "area_m2": "98.200",
        "area_m2_extenso": "noventa e oito mil e duzentos",
        "prazo_arrendamento": "25",
        "prazo_arrendamento_extenso": "vinte e cinco",

        # Contato Visita Técnica
        "contato_visita_nome": "João Silva",
        "contato_visita_cargo": "Gerente de Operações",
        "contato_visita_endereco": "Av. Conselheiro Nébias, 123 - Santos/SP",
        "contato_visita_email": "visitas@portosantos.gov.br",

        # Valores Financeiros
        "valor_garantia": "5.000.000,00",
        "valor_garantia_extenso": "cinco milhões de reais",
        "remuneracao_b3": "350.000,00",
        "remuneracao_b3_extenso": "trezentos e cinquenta mil reais",
        "remuneracao_estruturadora": "1.200.000,00",
        "remuneracao_estruturadora_extenso": "um milhão e duzentos mil reais",
        "remuneracao_ap": "500.000,00",
        "remuneracao_ap_extenso": "quinhentos mil reais",
        "valor_capital_social": "10.000.000,00",
        "valor_capital_social_extenso": "dez milhões de reais",

        # Períodos do Cronograma (Edital)
        "inicio_esclarecimento": "26/02/2026",
        "fim_esclarecimento": "01/03/2026",
        "inicio_impugnacao": "26/02/2026",
        "fim_impugnacao": "05/03/2026",
        "data_divulgacao_ata_impugnacao": "08/03/2026",
    }

    print("Substituindo variáveis Jinja2 no documento...")
    doc.render(dados_teste)
    
    doc.save(output_path)
    print(f"Sucesso! Documento salvo na pasta atual com o nome: {output_path}")

if __name__ == "__main__":
    gerar_minuta_teste()
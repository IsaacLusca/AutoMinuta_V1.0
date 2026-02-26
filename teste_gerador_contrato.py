from docxtpl import DocxTemplate
import os

def gerar_minuta_contrato_teste():
    # Caminho do arquivo de template do contrato
    template_path = "testes/MINUTA DE CONTRATO.docx" 
    output_path = "resultado_teste_contrato.docx"

    print(f"Carregando o template: {template_path}...")
    
    if not os.path.exists(template_path):
        print(f"ERRO: Arquivo '{template_path}' não encontrado!")
        print("Certifique-se de que o caminho e o nome do arquivo estão corretos.")
        return

    doc = DocxTemplate(template_path)

    # Dicionário simulando o 'form.cleaned_data' vindo do Django
    dados_teste = {
        # Informações Gerais do Leilão
        "leilao": "01/2026",
        "arrendamento": "Arrendamento de Instalação Portuária",
        "perfil_da_carga": "Granel Sólido Vegetal",
        "cargas_no_mme": "Trigo, Milho e Soja",
        "porto": "Porto de Santos",
        "codigo_area": "STS11",
        "poder_concedente": "Ministério de Portos e Aeroportos",
        "numero_edital": "01/2026",
        "numero_processo_administrativo": "50300.012345/2026-89",

        # Informações do Contrato
        "numero_contrato": "42",
        "ano_contrato": "2026",
        "data_base_reajuste": "julho de 2024",
        "data_base": "julho de 2024",
        
        # Datas de Assinatura
        "dia_assinatura": "25",
        "mes_assinatura": "outubro",
        "ano_assinatura": "2026",

        # Qualificação MPOR
        "sede_mpor": "Esplanada dos Ministérios, Bloco R, Brasília/DF",
        "nome_secretario_portos": "Carlos Silva",
        "qualificacao_secretario_portos": "brasileiro, casado, engenheiro",
        "decreto_nomeacao_secretario": "nº 10.123",
        "data_decreto_secretario": "15 de janeiro de 2023",
        "data_dou_secretario": "16 de janeiro de 2023",

        # Qualificação ANTAQ
        "sede_antaq": "SEPN Quadra 514, Conjunto E, Edifício ANTAQ, Brasília/DF",
        "nome_diretor_geral_antaq": "Eduardo Nery Machado Filho",
        "qualificacao_diretor_geral_antaq": "brasileiro, casado, servidor público",
        "ato_designacao_diretor_antaq": "nº 5.432",
        "data_dou_diretor_antaq": "20 de novembro de 2020",
        
        "nome_segundo_diretor": "Flávia Morais Takafashi",
        "ato_designacao_segundo_diretor": "nº 6.789",
        "data_dou_segundo_diretor": "10 de fevereiro de 2022",

        # Qualificação Autoridade Portuária
        "sede_autoridade_portuaria": "Avenida Conselheiro Rodrigues Alves, s/n, Macuco, Santos/SP",
        "cnpj_autoridade_portuaria": "44.837.522/0001-07",
        "nome_diretor_presidente_ap": "Anderson Pomini",
        "qualificacao_diretor_presidente_ap": "brasileiro, casado, advogado",
        "ato_designacao_diretor_ap": "Resolução do Conselho de Administração nº 12",
        "data_dou_diretor_ap": "05 de maio de 2023",

        # Qualificação Arrendatária
        "nome_arrendataria": "Santos Brasil Participações S.A.",
        "tipo_sociedade_arrendataria": "Sociedade de Propósito Específico",
        "municipio_arrendataria": "Santos",
        "estado_arrendataria": "SP",
        "sede_arrendataria": "Rua do Comércio, 100, Centro",
        "cnpj_arrendataria": "02.762.113/0001-31",
        "nome_representante_arrendataria": "João da Silva Sauro",
        "qualificacao_representante": "brasileiro, casado, administrador de empresas, portador do RG 11.222.333-4 e CPF 123.456.789-00",
        "endereco_comercial_representantes": "Rua do Comércio, 100, 5º andar, Centro, Santos/SP",

        # Valores Financeiros
        "valor_parcela_outorga": "15.000.000,00",
        "valor_parcela_outorga_extenso": "quinze milhões de reais",
    }

    print("Substituindo variáveis Jinja2 no documento do contrato...")
    doc.render(dados_teste)
    
    doc.save(output_path)
    print(f"Sucesso! Documento salvo na pasta atual com o nome: {output_path}")

if __name__ == "__main__":
    gerar_minuta_contrato_teste()
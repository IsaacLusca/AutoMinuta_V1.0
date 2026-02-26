from docxtpl import DocxTemplate
import PySimpleGUI as sg

doc = DocxTemplate("testes/testePreencher.docx")
context = {
    "nome_projeto": "Projeto de vendas",
    "data_criacao": "01/01/2024",
    "texto_simples": "Este é um texto simples para preencher o documento.",
    "descricao_longa": "Esta é uma descrição longa que pode conter várias linhas de texto. Ela é usada para demonstrar como preencher um documento do Word usando o docxtpl. Você pode adicionar quantas linhas quiser aqui, e o texto será formatado corretamente no documento final.",
    "status_teste": "Aprovado",
    }
doc.render(context)
doc.save("testes/testePreencher_Preenchido.docx")
import os
import django
import re

# 1. Configurar o ambiente do Django para o script rodar fora do servidor
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoMinuta.settings")
django.setup()

from gerador_avancado.models import BlocoPadrao, TipoBloco

def popular_banco(filepath):
    print(f"Lendo o arquivo: {filepath}...")
    
    with open(filepath, "r", encoding="latin-1") as f:
        content = f.read()

    # Limpeza inicial: remove tags HTML que vieram na extração do PDF
    content = re.sub(r'<[^>]+>', '', content)
    
    # Divide o texto inteiro em parágrafos
    paragrafos = re.split(r"\n\s*\n", content)
    
    print("Limpando banco de dados atual de BlocoPadrao...")
    BlocoPadrao.objects.all().delete()
    
    current_capitulo = None
    current_secao = None
    current_subsecao = None
    ordem_global = 10 
    
    count_blocos = 0

    for p in paragrafos:
        p = p.strip()
        if not p:
            continue
            
        if p.startswith("CAPÍTULO") or p.startswith("PREÂMBULO") or p.startswith("SUMÁRIO"):
            titulo_bloco = p.split("\n")[0].strip() 
            
            current_capitulo = BlocoPadrao.objects.create(
                tipo=TipoBloco.CAPITULO,
                titulo=titulo_bloco,
                conteudo="", 
                bloco_pai=None,
                ordem_padrao=ordem_global,
                obrigatorio=True 
            )
            current_secao = None
            current_subsecao = None
            count_blocos += 1
            print(f"Criado: {titulo_bloco}")

        elif p.startswith("Seção") or p.startswith("Apêndice"):
            titulo_bloco = p.split("\n")[0].strip()
            
            current_secao = BlocoPadrao.objects.create(
                tipo=TipoBloco.SECAO,
                titulo=titulo_bloco,
                conteudo="",
                bloco_pai=current_capitulo,
                ordem_padrao=ordem_global
            )
            current_subsecao = None
            count_blocos += 1

        elif p.startswith("Subseção"):
            titulo_bloco = p.split("\n")[0].strip()
            
            pai = current_secao if current_secao else current_capitulo
            
            current_subsecao = BlocoPadrao.objects.create(
                tipo=TipoBloco.SUBSECAO,
                titulo=titulo_bloco,
                conteudo="",
                bloco_pai=pai,
                ordem_padrao=ordem_global
            )
            count_blocos += 1

        else:
            pai_atual = current_subsecao or current_secao or current_capitulo
            
            if not pai_atual:
                pai_atual = BlocoPadrao.objects.create(
                    tipo=TipoBloco.CAPITULO,
                    titulo="INTRODUÇÃO (Sem Capítulo)",
                    ordem_padrao=ordem_global
                )
                current_capitulo = pai_atual

            conteudo_html = f"<p>{p.replace(chr(10), '<br>')}</p>"

            BlocoPadrao.objects.create(
                tipo=TipoBloco.CLAUSULA,
                titulo="", 
                conteudo=conteudo_html,
                bloco_pai=pai_atual,
                ordem_padrao=ordem_global
            )
            count_blocos += 1

        ordem_global += 10 

    print(f"\nSucesso! {count_blocos} blocos foram importados no banco de dados.")

if __name__ == "__main__":
    caminho_arquivo = "MINUTA-DE-EDITAL.txt"
    
    if os.path.exists(caminho_arquivo):
        popular_banco(caminho_arquivo)
    else:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
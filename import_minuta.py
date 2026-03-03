import os
import django
import re

# CONFIGURAR DJANGO
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoMinuta.settings")
django.setup()

from gerador_avancado.models import BlocoPadrao, TipoBloco


def limpar_numero_clausula(texto):
    # Remove padrões tipo 1.1 ou 1.1.1 do começo
    return re.sub(r'^\d+(\.\d+)+\s*[-–—]?\s*', '', texto).strip()


def popular_banco(filepath):
    print(f"Lendo: {filepath}")

    with open(filepath, "r", encoding="latin-1") as f:
        content = f.read()

    # Remove qualquer HTML
    content = re.sub(r'<[^>]+>', '', content)

    # Divide em blocos por linha dupla
    paragrafos = re.split(r"\n\s*\n", content)

    print("Limpando BlocoPadrao...")
    BlocoPadrao.objects.all().delete()

    current_capitulo = None
    current_secao = None
    current_subsecao = None
    ordem_global = 10
    count = 0

    for p in paragrafos:
        p = p.strip()
        if not p:
            continue

        linha = p.split("\n")[0].strip()

        # ================= CAPÍTULO =================
        if linha.upper().startswith("CAPÍTULO"):
            current_capitulo = BlocoPadrao.objects.create(
                tipo=TipoBloco.CAPITULO,
                titulo=linha,
                conteudo="",
                bloco_pai=None,
                ordem_padrao=ordem_global,
                obrigatorio=True
            )
            current_secao = None
            current_subsecao = None
            count += 1

        # ================= SEÇÃO =================
        elif linha.startswith("Seção"):
            current_secao = BlocoPadrao.objects.create(
                tipo=TipoBloco.SECAO,
                titulo=linha,
                conteudo="",
                bloco_pai=current_capitulo,
                ordem_padrao=ordem_global
            )
            current_subsecao = None
            count += 1

        # ================= SUBSEÇÃO =================
        elif linha.startswith("Subseção"):
            pai = current_secao if current_secao else current_capitulo

            current_subsecao = BlocoPadrao.objects.create(
                tipo=TipoBloco.SUBSECAO,
                titulo=linha,
                conteudo="",
                bloco_pai=pai,
                ordem_padrao=ordem_global
            )
            count += 1

        # ================= CLÁUSULA =================
        else:
            # Só considera como cláusula se começar com número tipo 1.1 ou 1.1.1
            if re.match(r'^\d+(\.\d+)+', linha):
                pai = current_subsecao or current_secao or current_capitulo

                if not pai:
                    continue  # ignora lixo antes de existir capítulo

                titulo_limpo = limpar_numero_clausula(linha)

                conteudo_html = f"<p>{p.replace(chr(10), '<br>')}</p>"

                BlocoPadrao.objects.create(
                    tipo=TipoBloco.CLAUSULA,
                    titulo=titulo_limpo,
                    conteudo=conteudo_html,
                    bloco_pai=pai,
                    ordem_padrao=ordem_global
                )
                count += 1

        ordem_global += 10

    print(f"\nImportação concluída. {count} blocos criados.")


if __name__ == "__main__":
    caminho = "MINUTA-DE-EDITAL.txt"

    if os.path.exists(caminho):
        popular_banco(caminho)
    else:
        print("Arquivo não encontrado.")
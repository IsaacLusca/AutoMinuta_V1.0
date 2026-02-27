from __future__ import annotations

from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from gerarMinuta.models import MinutaTemplate, Section


class Command(BaseCommand):
    help = "Importa a estrutura padrão da MINUTA-DE-EDITAL.txt para Sections ligadas a um MinutaTemplate 'edital-padrao'."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--path",
            type=str,
            default="testes/MINUTA-DE-EDITAL.txt",
            help="Caminho para o arquivo TXT da minuta de edital (relativo ao BASE_DIR).",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        txt_rel = options["path"]
        txt_path = Path(settings.BASE_DIR) / txt_rel

        if not txt_path.exists():
            self.stderr.write(self.style.ERROR(f"Arquivo não encontrado: {txt_path}"))
            return

        self.stdout.write(f"Lendo arquivo: {txt_path}")
        # O arquivo exportado do Word pode não estar em UTF-8; latin-1 costuma funcionar bem para PT-BR.
        with txt_path.open("r", encoding="latin-1", errors="ignore") as f:
            lines = [line.rstrip("\n") for line in f]

        blocks: list[dict[str, Any]] = []
        current_cap_idx: int | None = None
        current_sec_idx: int | None = None

        def start_block(level: int, title: str, parent_idx: int | None) -> int:
            blocks.append(
                {
                    "level": level,
                    "title": title.strip(),
                    "parent_idx": parent_idx,
                    "body_lines": [],
                }
            )
            return len(blocks) - 1

        for line in lines:
            stripped = line.strip()

            # detecta cabeçalho de capítulo
            if stripped.startswith("CAPÍTULO ") or stripped.startswith("CAPITULO "):
                current_cap_idx = start_block(1, stripped, None)
                current_sec_idx = None
                continue

            # detecta Seção / Subseção
            if stripped.startswith("Seção ") or stripped.startswith("Subseção "):
                # seção/subseção sempre é filha do capítulo atual, se existir
                parent = current_cap_idx
                current_sec_idx = start_block(2, stripped, parent)
                continue

            # linhas de corpo
            target_idx: int | None = None
            if current_sec_idx is not None:
                target_idx = current_sec_idx
            elif current_cap_idx is not None:
                target_idx = current_cap_idx

            if target_idx is not None:
                blocks[target_idx]["body_lines"].append(line)

        self.stdout.write(f"Blocos detectados: {len(blocks)}")

        template, created = MinutaTemplate.objects.get_or_create(
            slug="edital-padrao",
            defaults={
                "name": "Edital Padrão",
                "kind": MinutaTemplate.Kind.EDITAL,
                "version": 1,
                "is_published": False,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Criado MinutaTemplate '{template}'"))
        else:
            self.stdout.write(f"Usando MinutaTemplate existente: {template}")

        # limpa seções antigas desse template para evitar duplicação
        deleted, _ = Section.objects.filter(template=template).delete()
        if deleted:
            self.stdout.write(f"Removidas {deleted} seções antigas para '{template.slug}'.")

        created_sections: list[Section] = []

        # primeiro passa: criar todas as seções sem parent
        for idx, block in enumerate(blocks):
            parent_idx = block["parent_idx"]
            # vamos definir order de forma incremental por pai
            if parent_idx is None:
                order = sum(1 for b in blocks[:idx] if b["parent_idx"] is None)
            else:
                order = sum(1 for b in blocks[:idx] if b["parent_idx"] == parent_idx)

            section = Section(
                template=template,
                parent=None,  # vamos setar depois
                order=order,
                title=block["title"],
                body="\n".join(block["body_lines"]).strip("\n"),
            )
            created_sections.append(section)

        # salvar para ter IDs
        Section.objects.bulk_create(created_sections)
        created_sections = list(Section.objects.filter(template=template).order_by("id"))

        # mapear índice de bloco -> Section
        idx_to_section: dict[int, Section] = {
            idx: created_sections[idx] for idx in range(len(blocks))
        }

        # segunda passada: atualizar parents
        updates: list[Section] = []
        for idx, block in enumerate(blocks):
            parent_idx = block["parent_idx"]
            if parent_idx is None:
                continue
            sec = idx_to_section[idx]
            sec.parent = idx_to_section.get(parent_idx)
            updates.append(sec)

        Section.objects.bulk_update(updates, ["parent"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Importação concluída: {len(created_sections)} seções criadas para '{template.slug}'."
            )
        )


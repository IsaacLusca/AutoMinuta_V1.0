from __future__ import annotations

import io
import re
from dataclasses import dataclass

from .models import MinutaTemplate, Section


_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_-]+)\s*\}\}")


def _render_placeholders(text: str, values: dict[str, object]) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        value = values.get(key, "")
        if value is None:
            return ""
        return str(value)

    return _PLACEHOLDER_RE.sub(repl, text)


@dataclass(frozen=True)
class RenderedSection:
    number: str
    level: int
    title: str
    body: str


def _build_tree(sections: list[Section]) -> tuple[dict[int | None, list[Section]], dict[int, Section]]:
    by_parent: dict[int | None, list[Section]] = {}
    by_id: dict[int, Section] = {}
    for s in sections:
        by_id[s.id] = s
        by_parent.setdefault(s.parent_id, []).append(s)
    for _, items in by_parent.items():
        items.sort(key=lambda x: (x.order, x.id))
    return by_parent, by_id


def _walk_numbered(
    by_parent: dict[int | None, list[Section]],
    parent_id: int | None,
    prefix: list[int],
    level: int,
) -> list[RenderedSection]:
    rendered: list[RenderedSection] = []
    children = by_parent.get(parent_id, [])
    for idx, s in enumerate(children, start=1):
        current_prefix = [*prefix, idx]
        number = ".".join(str(n) for n in current_prefix)
        rendered.append(
            RenderedSection(
                number=number,
                level=level,
                title=s.title or "",
                body=s.body or "",
            )
        )
        rendered.extend(_walk_numbered(by_parent, s.id, current_prefix, level + 1))
    return rendered


def build_corpo_minuta(
    template: MinutaTemplate,
    values: dict[str, object],
    included_section_ids: set[int] | None = None,
) -> str:
    """
    Gera um texto único representando a minuta inteira (capítulos + seções),
    com numeração recalculada e placeholders substituídos.
    Pensado para ser injetado em um placeholder único do DOCX via docxtpl
    (ex.: {{ corpo_minuta }}).
    """
    sections = list(template.sections.select_related("parent").all())

    if included_section_ids is not None:
        filtered: list[Section] = []
        for s in sections:
            # capítulos (sem parent) sempre entram; demais só se estiverem marcados
            if s.parent_id is None or s.id in included_section_ids:
                filtered.append(s)
        sections = filtered

    by_parent, _ = _build_tree(sections)
    rendered = _walk_numbered(by_parent, None, [], 1)

    lines: list[str] = []

    for item in rendered:
        heading_text = item.number
        if item.title.strip():
            heading_text = f"{heading_text} {item.title.strip()}"
        heading_text = _render_placeholders(heading_text, values)

        lines.append(heading_text)

        body_text = _render_placeholders(item.body, values).strip("\n")
        if body_text:
            lines.append(body_text)

        # linha em branco entre seções
        lines.append("")

    # remove espaços em branco extra no final
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)



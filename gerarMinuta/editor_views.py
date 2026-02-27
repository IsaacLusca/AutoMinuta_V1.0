from __future__ import annotations

import json
import os

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from docxtpl import DocxTemplate

from .ai_extract import extract_placeholders_from_pdf
from .docx_renderer import build_corpo_minuta
from .editor_forms import (
    MinutaTemplateForm,
    PlaceholderFieldForm,
    SectionForm,
    TemplatePlaceholderForm,
    build_values_form,
)
from .models import MinutaTemplate, PlaceholderField, Section, TemplatePlaceholder
import io


def _numbered_sections(template: MinutaTemplate) -> list[tuple[str, int, Section]]:
    sections = list(template.sections.select_related("parent").all())
    by_parent: dict[int | None, list[Section]] = {}
    for s in sections:
        by_parent.setdefault(s.parent_id, []).append(s)
    for items in by_parent.values():
        items.sort(key=lambda x: (x.order, x.id))

    out: list[tuple[str, int, Section]] = []

    def walk(parent_id: int | None, prefix: list[int], level: int) -> None:
        children = by_parent.get(parent_id, [])
        for idx, s in enumerate(children, start=1):
            current_prefix = [*prefix, idx]
            number = ".".join(str(n) for n in current_prefix)
            out.append((number, level, s))
            walk(s.id, current_prefix, level + 1)

    walk(None, [], 1)
    return out


def template_list(request: HttpRequest) -> HttpResponse:
    templates = MinutaTemplate.objects.all().order_by("-updated_at")
    return render(request, "editor/template_list.html", {"templates": templates})


def template_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MinutaTemplateForm(request.POST)
        if form.is_valid():
            template = form.save()
            return redirect("editor_template_detail", slug=template.slug)
    else:
        form = MinutaTemplateForm()

    return render(request, "editor/template_form.html", {"form": form, "mode": "create"})


def template_detail(request: HttpRequest, slug: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    placeholders = template.template_placeholders.select_related("field").all()
    numbered = _numbered_sections(template)
    fields = PlaceholderField.objects.all().order_by("key")
    return render(
        request,
        "editor/template_detail.html",
        {
            "template": template,
            "placeholders": placeholders,
            "numbered_sections": numbered,
            "fields": fields,
        },
    )


def template_edit(request: HttpRequest, slug: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    if request.method == "POST":
        form = MinutaTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect("editor_template_detail", slug=template.slug)
    else:
        form = MinutaTemplateForm(instance=template)
    return render(
        request,
        "editor/template_form.html",
        {"form": form, "mode": "edit", "template": template},
    )


def placeholder_list(request: HttpRequest) -> HttpResponse:
    fields = PlaceholderField.objects.all().order_by("key")
    return render(request, "editor/placeholder_list.html", {"fields": fields})


def placeholder_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PlaceholderFieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("editor_placeholder_list")
    else:
        form = PlaceholderFieldForm()
    return render(request, "editor/placeholder_form.html", {"form": form})


def template_placeholder_add(request: HttpRequest, slug: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    if request.method != "POST":
        return redirect("editor_template_detail", slug=template.slug)

    form = TemplatePlaceholderForm(request.POST)
    if form.is_valid():
        binding: TemplatePlaceholder = form.save(commit=False)
        binding.template = template
        binding.save()
    return redirect("editor_template_detail", slug=template.slug)


def template_placeholder_remove(request: HttpRequest, slug: str, binding_id: int) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    binding = get_object_or_404(TemplatePlaceholder, id=binding_id, template=template)
    if request.method == "POST":
        binding.delete()
    return redirect("editor_template_detail", slug=template.slug)


def section_create(request: HttpRequest, slug: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    if request.method == "POST":
        form = SectionForm(request.POST)
        form.fields["parent"].queryset = template.sections.all()
        if form.is_valid():
            section: Section = form.save(commit=False)
            section.template = template
            section.save()
            return redirect("editor_template_detail", slug=template.slug)
    else:
        form = SectionForm()
        form.fields["parent"].queryset = template.sections.all()

    return render(request, "editor/section_form.html", {"form": form, "template": template})


def section_edit(request: HttpRequest, slug: str, section_id: int) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    section = get_object_or_404(Section, id=section_id, template=template)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect("editor_template_detail", slug=template.slug)
    else:
        form = SectionForm(instance=section)
        form.fields["parent"].queryset = template.sections.exclude(id=section.id)

    return render(
        request,
        "editor/section_form.html",
        {"form": form, "template": template, "section": section},
    )


def section_delete(request: HttpRequest, slug: str, section_id: int) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    section = get_object_or_404(Section, id=section_id, template=template)
    if request.method == "POST":
        section.delete()
    return redirect("editor_template_detail", slug=template.slug)


def section_move(request: HttpRequest, slug: str, section_id: int, direction: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)
    section = get_object_or_404(Section, id=section_id, template=template)
    if request.method != "POST":
        return redirect("editor_template_detail", slug=template.slug)

    siblings = list(
        Section.objects.filter(template=template, parent_id=section.parent_id).order_by("order", "id")
    )
    idx = next((i for i, s in enumerate(siblings) if s.id == section.id), None)
    if idx is None:
        return redirect("editor_template_detail", slug=template.slug)

    if direction == "up" and idx > 0:
        other = siblings[idx - 1]
    elif direction == "down" and idx < len(siblings) - 1:
        other = siblings[idx + 1]
    else:
        return redirect("editor_template_detail", slug=template.slug)

    section.order, other.order = other.order, section.order
    section.save(update_fields=["order", "updated_at"])
    other.save(update_fields=["order", "updated_at"])
    return redirect("editor_template_detail", slug=template.slug)


def template_generate_docx(request: HttpRequest, slug: str) -> HttpResponse:
    template = get_object_or_404(MinutaTemplate, slug=slug)

    mensagem_ia: str | None = None
    tipo_mensagem: str = "secondary"

    if request.method == "POST" and "btn_analisar_ia" in request.POST:
        pdf = request.FILES.get("arquivo_pdf")
        keys = list(
            template.template_placeholders.select_related("field").values_list("field__key", flat=True)
        )
        if not pdf:
            mensagem_ia = "Selecione um PDF antes de analisar."
            tipo_mensagem = "warning"
        elif not keys:
            mensagem_ia = "Associe campos ao template antes de usar a IA."
            tipo_mensagem = "warning"
        else:
            try:
                extracted = extract_placeholders_from_pdf(pdf, keys)
                request.session[f"editor_ai_extracted:{template.slug}"] = json.dumps(extracted, ensure_ascii=False)
                mensagem_ia = "Campos preenchidos com sucesso!"
                tipo_mensagem = "success"
            except Exception as e:
                mensagem_ia = f"Erro na IA: {str(e)}"
                tipo_mensagem = "danger"

    extracted_initial: dict[str, object] = {}
    raw = request.session.get(f"editor_ai_extracted:{template.slug}")
    if raw:
        try:
            extracted_initial = json.loads(raw)
        except Exception:
            extracted_initial = {}

    numbered_sections = _numbered_sections(template)

    if request.method == "POST":
        if "btn_analisar_ia" in request.POST:
            values_form = build_values_form(template, initial=extracted_initial)
            return render(
                request,
                "editor/template_generate.html",
                {
                    "template": template,
                    "values_form": values_form,
                    "mensagem_ia": mensagem_ia,
                    "tipo_mensagem": tipo_mensagem,
                },
            )

        values_form = build_values_form(template, initial=extracted_initial)
        values_form = values_form.__class__(request.POST)
        if values_form.is_valid():
            # seções marcadas (apenas não-raiz têm checkbox)
            raw_ids = request.POST.getlist("section_ids")
            included_ids: set[int] = set()
            for raw_id in raw_ids:
                try:
                    included_ids.add(int(raw_id))
                except ValueError:
                    continue

            values = values_form.cleaned_data

            # 1) monta corpo_minuta com seções escolhidas
            corpo = build_corpo_minuta(template, values, included_section_ids=included_ids or None)

            # 2) escolhe o arquivo DOCX base conforme o tipo de template
            if template.kind == MinutaTemplate.Kind.EDITAL:
                template_path = os.path.join("testes", "MINUTA DE EDITAL.docx")
            elif template.kind == MinutaTemplate.Kind.CONTRATO:
                template_path = os.path.join("testes", "MINUTA DE CONTRATO.docx")
            else:
                # fallback: usa o de edital
                template_path = os.path.join("testes", "MINUTA DE EDITAL.docx")

            doc = DocxTemplate(template_path)
            contexto = {
                **values,
                "corpo_minuta": corpo,
            }
            doc.render(contexto)

            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            response = HttpResponse(
                buffer.read(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            response["Content-Disposition"] = f'attachment; filename="{template.slug}.docx"'
            return response
    else:
        values_form = build_values_form(template, initial=extracted_initial)

    return render(
        request,
        "editor/template_generate.html",
        {
            "template": template,
            "values_form": values_form,
            "mensagem_ia": mensagem_ia,
            "tipo_mensagem": tipo_mensagem,
            "numbered_sections": numbered_sections,
        },
    )


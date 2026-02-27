from __future__ import annotations

from django import forms

from .models import MinutaTemplate, PlaceholderField, Section, TemplatePlaceholder


class MinutaTemplateForm(forms.ModelForm):
    class Meta:
        model = MinutaTemplate
        fields = ["name", "kind", "version", "is_published"]


class PlaceholderFieldForm(forms.ModelForm):
    class Meta:
        model = PlaceholderField
        fields = ["key", "label", "field_type", "required", "help_text"]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["parent", "order", "title", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }


class TemplatePlaceholderForm(forms.ModelForm):
    class Meta:
        model = TemplatePlaceholder
        fields = ["field", "order"]


def build_values_form(template: MinutaTemplate, *, initial: dict | None = None) -> forms.Form:
    initial = initial or {}

    fields: list[tuple[int, PlaceholderField]] = [
        (tp.order, tp.field) for tp in template.template_placeholders.select_related("field").all()
    ]
    fields.sort(key=lambda x: (x[0], x[1].key))

    form_fields: dict[str, forms.Field] = {}
    for _, f in fields:
        if f.field_type == PlaceholderField.FieldType.TEXTAREA:
            form_field: forms.Field = forms.CharField(
                label=f.label,
                required=f.required,
                help_text=f.help_text,
                widget=forms.Textarea(attrs={"rows": 3}),
            )
        elif f.field_type == PlaceholderField.FieldType.DATE:
            form_field = forms.DateField(
                label=f.label,
                required=f.required,
                help_text=f.help_text,
                widget=forms.DateInput(attrs={"type": "date"}),
            )
        elif f.field_type == PlaceholderField.FieldType.EMAIL:
            form_field = forms.EmailField(
                label=f.label,
                required=f.required,
                help_text=f.help_text,
            )
        elif f.field_type == PlaceholderField.FieldType.NUMBER:
            form_field = forms.DecimalField(
                label=f.label,
                required=f.required,
                help_text=f.help_text,
                decimal_places=2,
            )
        else:
            form_field = forms.CharField(
                label=f.label,
                required=f.required,
                help_text=f.help_text,
            )

        form_fields[f.key] = form_field

    DynamicForm = type(
        "MinutaValuesForm",
        (forms.Form,),
        form_fields,
    )
    return DynamicForm(initial=initial)


from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class MinutaTemplate(models.Model):
    class Kind(models.TextChoices):
        EDITAL = "edital", "Edital"
        CONTRATO = "contrato", "Contrato"
        OUTRO = "outro", "Outro"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.OUTRO)
    version = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "minuta"
            candidate = base
            i = 2
            while MinutaTemplate.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{i}"
                i += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} (v{self.version})"


class PlaceholderField(models.Model):
    class FieldType(models.TextChoices):
        TEXT = "text", "Texto"
        TEXTAREA = "textarea", "Texto longo"
        DATE = "date", "Data"
        EMAIL = "email", "Email"
        NUMBER = "number", "Número"
        CURRENCY = "currency", "Moeda"

    key = models.SlugField(max_length=80, unique=True)
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.TEXT)
    required = models.BooleanField(default=False)
    help_text = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.key} ({self.get_field_type_display()})"


class TemplatePlaceholder(models.Model):
    template = models.ForeignKey(MinutaTemplate, on_delete=models.CASCADE, related_name="template_placeholders")
    field = models.ForeignKey(PlaceholderField, on_delete=models.CASCADE, related_name="template_bindings")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("template", "field")]
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.template.slug}:{self.field.key}"


class Section(models.Model):
    template = models.ForeignKey(MinutaTemplate, on_delete=models.CASCADE, related_name="sections")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=300, blank=True)
    body = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["template", "parent", "order"]),
        ]

    def __str__(self) -> str:
        return self.title or f"Section {self.pk}"


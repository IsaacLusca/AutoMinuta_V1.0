from django.contrib import admin

from .models import MinutaTemplate, PlaceholderField, Section, TemplatePlaceholder


class TemplatePlaceholderInline(admin.TabularInline):
    model = TemplatePlaceholder
    extra = 0


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ("parent", "order", "title")


@admin.register(MinutaTemplate)
class MinutaTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "version", "is_published", "slug", "updated_at")
    list_filter = ("kind", "is_published")
    search_fields = ("name", "slug")
    inlines = [TemplatePlaceholderInline, SectionInline]


@admin.register(PlaceholderField)
class PlaceholderFieldAdmin(admin.ModelAdmin):
    list_display = ("key", "label", "field_type", "required", "updated_at")
    list_filter = ("field_type", "required")
    search_fields = ("key", "label")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("template", "parent", "order", "title", "updated_at")
    list_filter = ("template",)
    search_fields = ("title", "body")


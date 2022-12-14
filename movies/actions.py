from django.contrib import admin


@admin.action(description='Make selected movies drafts')
def make_draft(modeladmin, request, queryset):
    queryset.update(is_draft=True)

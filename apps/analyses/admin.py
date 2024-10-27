from django.contrib import admin

from apps.analyses.models import Documents


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'page_number', 'price', 'paragraph_name', 'created_at')
    ordering = ('page_number', 'price')


admin.site.register(Documents, DocumentAdmin)

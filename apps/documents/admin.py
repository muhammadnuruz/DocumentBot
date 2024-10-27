from django.contrib import admin

from apps.documents.models import Types


class TypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    ordering = ('price', 'created_at')


admin.site.register(Types, TypesAdmin)

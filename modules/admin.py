from django.contrib import admin
from .models import (Modules)


class ModulesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'reference_url',
                    'created_at', 'updated_at')
    list_filter = ('active',)
    fieldsets = (
        ('Module Info', {
            'classes': ('wide',),
            'fields': ('name', 'tagline', 'description', 'image_url', 'active', 'reference_url')
        }),
    )

    search_fields = ('reference_url',)
    ordering = ('pk',)


admin.site.register(Modules, ModulesAdmin)

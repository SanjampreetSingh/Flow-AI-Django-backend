from django.contrib import admin
from .models import (Apps)


class AppsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'reference_url', 'ready_apis',
        'custom_apis', 'notebook', 'active', 'created_at', 'updated_at'
    )
    readonly_fields = ('ready_apis', 'custom_apis', 'notebook', 'apikey_value', 'apikey_id',
                       'usage_plans', 'reference_url')
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('App Info', {
            'classes': ('wide',),
            'fields': ('name', 'description', 'active')
        }),
        ('Active Models in App  (Do Not Modify)', {
            'classes': ('wide',),
            'fields': ('ready_apis', 'custom_apis', 'notebook', )
        }),
        ('Cloud Details in App (Do Not Modify)', {
            'classes': ('wide',),
            'fields': ('apikey_value', 'apikey_id', 'usage_plans', 'reference_url')
        }),
    )
    search_fields = ('reference_url', 'user__email')
    ordering = ('updated_at',)
    list_filter = ('active', 'user__complete', 'user__verified')


admin.site.register(Apps, AppsAdmin)

from django.contrib import admin
from .models import (ReadyApis, ReadyApiCategory, ReadyApiMedia)


class ReadyApisAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'reference_url',
                    'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    readonly_fields = ('recommendations',)
    fieldsets = (
        ('Ready Api Info', {
            'classes': ('wide',),
            'fields': ('name', 'category', 'active', 'reference_url', 'tagline', 'description', 'image_url', 'use_cases', 'tag', 'recommendations')
        }),
        ('Cloud Details of Ready Api (Do Not Modify)', {
            'classes': ('wide',),
            'fields': ('cloud_url', 'usage_plan_id', 'apikey_stage')
        }),
        ('Pricing per API call', {
            'classes': ('wide',),
            'fields': ('price',)
        }),

    )

    search_fields = ('reference_url',)
    ordering = ('pk',)


class ReadyApiMediaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'url', 'created_at', 'updated_at')
    list_filter = ('category__name',)
    fieldsets = (
        ('Ready Api Media Info', {
            'classes': ('wide',),
            'fields': ('category', 'media', 'url',)
        }),
    )
    ordering = ('pk',)


class ReadyApiCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    fieldsets = (
        ('Ready Api Category Info', {
            'classes': ('wide',),
            'fields': ('name',)
        }),
    )
    search_fields = ('name',)
    ordering = ('pk',)


admin.site.register(ReadyApis, ReadyApisAdmin)
admin.site.register(ReadyApiCategory, ReadyApiCategoryAdmin)
admin.site.register(ReadyApiMedia, ReadyApiMediaAdmin)

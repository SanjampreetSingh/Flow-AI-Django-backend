from django.contrib import admin
from .models import (ReadyApiUsagePerModels)


class ReadyApiUsagePerModelsAdmin(admin.ModelAdmin):
    list_display = ('app', 'api', 'usage', 'active',
                    'created_at', 'updated_at')
    list_filter = ('active',)
    fieldsets = (
        (None, {'fields': ('app', 'api')}),
        ('Bucket Info', {
            'classes': ('wide',),
            'fields': ('usage', 'active')
        }),
    )

    search_fields = ('app__reference_url', 'app__user__email')
    ordering = ('app__id',)


admin.site.register(ReadyApiUsagePerModels, ReadyApiUsagePerModelsAdmin)

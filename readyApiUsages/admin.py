from django.contrib import admin
from .models import (ReadyApiUsageBuckets)


class ReadyApiUsageBucketsAdmin(admin.ModelAdmin):
    list_display = ('app', 'user', 'bucket', 'usage', 'threshold',
                    'active', 'created_at', 'updated_at')
    list_filter = ('active', 'user__complete')
    fieldsets = (
        (None, {'fields': ('app', 'user')}),
        ('Bucket Info', {
            'classes': ('wide',),
            'fields': ('bucket', 'usage', 'threshold', 'active')
        }),
    )

    search_fields = ('app__reference_url', 'user__email')
    ordering = ('app__id',)


admin.site.register(ReadyApiUsageBuckets, ReadyApiUsageBucketsAdmin)

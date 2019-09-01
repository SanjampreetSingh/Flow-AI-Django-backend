from django.contrib import admin
from .models import (Apis, ApiCategory, ApiImage)


class ApiAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'category', 'trial',
                    'active', 'recommendations', 'price')

    class Meta:
        model = Apis


admin.site.register(Apis, ApiAdmin)
admin.site.register(ApiCategory)
admin.site.register(ApiImage)

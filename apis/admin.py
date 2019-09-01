from django.contrib import admin
from .models import (Api, ApiCategory, ApiImage)


class ApiAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'category', 'trial',
                    'active', 'recommendations', 'price')

    class Meta:
        model = Api


admin.site.register(Api, ApiAdmin)
admin.site.register(ApiCategory)
admin.site.register(ApiImage)

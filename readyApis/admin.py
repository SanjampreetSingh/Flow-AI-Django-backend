from django.contrib import admin
from .models import (ReadyApis, ReadyApiCategory, ReadyApiMedia)


class ReadyApiAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'category', 'active', 'recommendations', 'price')

    class Meta:
        model = ReadyApis


admin.site.register(ReadyApis, ReadyApiAdmin)
admin.site.register(ReadyApiCategory)
admin.site.register(ReadyApiMedia)

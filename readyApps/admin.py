from django.contrib import admin
from .models import (ReadyApps)


class ReadyAppAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'active')

    class Meta:
        model = ReadyApps


admin.site.register(ReadyApps, ReadyAppAdmin)

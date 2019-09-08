from django.contrib import admin
from .models import (Modules)


class ModuleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'active')

    class Meta:
        model = Modules


admin.site.register(Modules, ModuleAdmin)

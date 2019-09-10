from django.contrib import admin
from .models import (Apps)


class AppAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'active')

    class Meta:
        model = Apps


admin.site.register(Apps, AppAdmin)

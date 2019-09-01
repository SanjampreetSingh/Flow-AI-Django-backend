from django.contrib import admin
from .models import (Plans)


class PlanAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Plans, PlanAdmin)

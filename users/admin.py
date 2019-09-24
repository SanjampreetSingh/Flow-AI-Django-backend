from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from .forms import UserAdminCreationForm, UserAdminChangeForm
from . import models


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'user_type', 'active', 'staff',
                    'admin', 'verified', 'complete', 'last_login', 'created_at')
    list_filter = ('admin', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Info', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('admin', 'staff',
                                    'active', 'verified', 'complete',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(models.Users, UserAdmin)

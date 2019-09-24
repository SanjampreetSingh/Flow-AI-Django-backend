from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = 'Flow Admin'
admin.site.site_title = 'Flow Admin'
admin.site.index_title = 'Flow'


admin.site.unregister(Group)

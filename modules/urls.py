from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('module/', views.ModuleList.as_view(),
         name="module_list"),
    re_path(r'^module/(?P<reference_url>[-\w]+)/$',
            views.ModuleDetails.as_view(), name="module_details"),
]

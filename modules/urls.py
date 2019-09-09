from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('module/', views.ModuleList.as_view(),
         name="module_list"),
    re_path(r'^products/(?P<pk>\d+)$',
            views.ModuleDetails.as_view(), name="module_details"),
]

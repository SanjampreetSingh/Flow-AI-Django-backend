from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

urlpatterns = [
    # User PREFIX
    path('user/', include([
        # Plan URL
        path('plan/', views.PlanListUser.as_view(), name="user_plan_list"),
    ])),

    # Frontend PREFIX
    path('frontend/', include([
        # Plan URL
        path('plan/', views.PlanListFrontend.as_view(),
             name='public_plan_list'),
    ])),
]

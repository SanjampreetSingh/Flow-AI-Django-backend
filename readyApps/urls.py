from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('ready/app', views.ReadyAppViewSet)
router.register('ready/app/image', views.ReadyAppImageViewSet)
urlpatterns = [
    # User PREFIX
    path('user/', include([
        path('', include(router.urls)),
        path('ready/app/actions', views.actionsApiUsagePlan),
    ])),
]

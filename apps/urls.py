from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('app', views.AppViewSet)
router.register('app/image', views.AppImageViewSet)
urlpatterns = [
    # User PREFIX
    path('user/', include([
        path('', include(router.urls)),
    ])),
]

from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

# router.register('profile/picture', views.ProfilePictureViewSet)
urlpatterns = [
    # User PREFIX (Closed URLs)
    path('user/', include([
        path('', include(router.urls)),
    ])),
]

from django.urls import path, include, re_path
from rest_framework_jwt.views import verify_jwt_token
from . import views


urlpatterns = [
    # check user
    path('check/user/', views.checkUser, name='user_register'),

    # Register
    path('register/', views.register, name='user_register'),

    # Activate
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.verifyEmail, name='activate'),

    # Login
    path('authenticate/', views.LoginAPI.as_view()),

    # Auth
    path('verify/', verify_jwt_token),

    path('get/user/', views.get_user, name='get_user'),

    path('oauth/login/', views.SocialLoginView.as_view())
]

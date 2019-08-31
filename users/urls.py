from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Register URL
    path('register/', views.register, name='user_register'),
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.verifyEmail, name='activate'),
    # path('confirm/', views.confirm_otp, name='confirm_otp'),
    # path('resend/', views.resend_otp, name='resend_otp'),
]

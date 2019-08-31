from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Register URL
    path('register/', views.register, name='user_register'),
    # path('confirm/', views.confirm_otp, name='confirm_otp'),
    # path('resend/', views.resend_otp, name='resend_otp'),
]

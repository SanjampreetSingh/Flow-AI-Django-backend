from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Register URL
    path('register/', views.register, name='user_register'),

    # Activate URL
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.verifyEmail, name='activate'),

    # Login URL
    path('authenticate/', views.Login.as_view()),
]

"""flow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
# From USER VIEW
from users.views import (
    verifyEmail,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comman.package_urls')),
    # Verify user email From USER VIEW
    re_path(
        r'^verify/email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', verifyEmail, name='verify_user_email'),
    re_path(r'^$', RedirectView.as_view(url='https://theflowai.com')),
    path('api/', include([
        path('auth/', include('rest_framework_social_oauth2.urls')),
        path('', include('comman.urls')),
    ])),
]

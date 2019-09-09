# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from users.models import (Users)
from .models import (Apps, AppImage)
from .serializer import (AppSerializer, AppImageSerializer)


class AppViewSet(viewsets.ModelViewSet):
    queryset = Apps.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


class AppImageViewSet(viewsets.ModelViewSet):
    queryset = AppImage.objects.all()
    serializer_class = AppImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

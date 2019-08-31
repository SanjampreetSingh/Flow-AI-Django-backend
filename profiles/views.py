from datetime import datetime

# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404
from django.shortcuts import render

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from .models import (Profiles)
from .serializer import (ProfileSerializer)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

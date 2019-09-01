from datetime import datetime

# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from users.models import (Users)
from .models import (Apis, ApiImage, ApiCategory)
from .serializer import (
    ApiSerializer, ApiImageSerializer, ApiCategorySerializer)


# Api's Image List
class ApiImageList(ListAPIView):
    permission_classes = (IsAuthenticated)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ApiImage.objects.all()
    serializer_class = ApiImageSerializer

    def get_queryset(self):
        data = self.request.data
        if 'category' in data:
            queryset = ApiImage.objects.filter(category=data.get('category'))
        elif 'api' in data:
            queryset = ApiImage.objects.filter(api=data.get('api'))
        else:
            queryset = ApiImage.objects.all()
        return queryset


class TrialApiImageList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ApiImage.objects.all().exclude(trial=False)
    serializer_class = ApiImageSerializer

    def get_queryset(self):
        data = self.request.data
        if 'category' in data:
            queryset = ApiImage.objects.filter(
                category=data.get('category')).exclude(trial=False)
        elif 'api' in data:
            queryset = ApiImage.objects.filter(
                api=data.get('api')).exclude(trial=False)
        else:
            queryset = ApiImage.objects.all().exclude(trial=False)
        return queryset

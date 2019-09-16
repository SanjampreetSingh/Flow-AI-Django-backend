# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from users.models import (Users)
from .models import (ReadyApis, ReadyApiMedia, ReadyApiCategory)
from .serializer import (
    ReadyApiSerializer, ReadyApiMediaSerializer, ReadyApiCategorySerializer)


# Ready Api's List
class ReadyApiList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApis.objects.all()
    serializer_class = ReadyApiSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = ReadyApis.objects.filter(category=category)
        else:
            queryset = ReadyApis.objects.all()
        return queryset


# Ready Api's Retrieve
class ReadyApiRetrieve(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApis.objects.all()
    serializer_class = ReadyApiSerializer


# Ready Api's Media List
class ReadyApiMediaList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApiMedia.objects.all()
    serializer_class = ReadyApiMediaSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = ReadyApiMedia.objects.filter(category=category)
        else:
            queryset = ReadyApiMedia.objects.all()
        return queryset


# Ready Api Category List
class ReadyApiCategoryList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApiCategory.objects.all()
    serializer_class = ReadyApiCategorySerializer
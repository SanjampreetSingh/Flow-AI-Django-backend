import json
import requests
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
from readyApps.models import (ReadyApps)
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

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReadyApiSerializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'message': 'Ready api list.',
                'data': {
                    'readyApis': serializer.data
                }
            },
            status=status.HTTP_200_OK)


# Ready Api's Retrieve
class ReadyApiRetrieve(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApis.objects.all()
    serializer_class = ReadyApiSerializer

    def retrieve(self, request):
        queryset = self.get_queryset()
        serializer = ReadyApiSerializer(queryset)
        return Response(
            {
                'success': True,
                'message': 'Ready api details.',
                'data': {
                    'readyApisMedia': serializer.data
                }
            },
            status=status.HTTP_200_OK)


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

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReadyApiMediaSerializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'message': 'Ready api media list.',
                'data': {
                    'readyApisMedia': serializer.data
                }
            },
            status=status.HTTP_200_OK)


# Ready Api Category List
class ReadyApiCategoryList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = ReadyApiCategory.objects.all()
    serializer_class = ReadyApiCategorySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReadyApiCategorySerializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'message': 'Ready api media list.',
                'data': {
                    'readyApisCategory': serializer.data
                }
            },
            status=status.HTTP_200_OK)


# Ready Api Demo
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def readyApiDemo(request):
    if request.method == 'POST':
        try:
            app = ReadyApps.objects.get(
                apikey_value=request.data.get('apikey'))
        except ReadyApps.DoesNotExist:
            return Response('App not found.', status=status.HTTP_404_NOT_FOUND)

        query = ReadyApis.objects.get(name=request.data.get('name'))

        api_data = {
            'data': request.data.get('data')
        }
        data = json.dumps(api_data)
        headers = {
            'x-api-key': request.data.get('apikey'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = requests.post(
            query.cloud_url, data=data, headers=headers)

        return Response(
            {
                'success': True,
                'message': 'Ready api demo.',
                'data': {
                    'demoData': req.json()
                }
            },
            status=status.HTTP_200_OK)

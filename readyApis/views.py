import json
import requests

# Django
from django.conf import settings

# Django Rest Framework Files
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from .models import (
    ReadyApis,
    ReadyApiMedia,
    ReadyApiCategory
)
from .serializer import (
    ReadyApiSerializer,
    ReadyApiMediaSerializer,
    ReadyApiCategorySerializer,
    ReadyApiDemoSerializer
)
from comman import response


# Ready Api's List
class ReadyApiList(ListAPIView):
    permission_classes = (AllowAny,)

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
        response_data = {
            'readyApis': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api list.', response_data, status.HTTP_200_OK)


# Ready Api's Retrieve
class ReadyApiRetrieve(RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'reference_url'

    def retrieve(self, request, reference_url):
        queryset = ReadyApis.objects.all()
        serializer = ReadyApiSerializer(queryset, many=True)
        response_data = {
            'readyApiData': serializer.data[0]
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api details.', response_data, status.HTTP_200_OK)


# Ready Api's Media List
class ReadyApiMediaList(ListAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = ReadyApiMedia.objects.filter(category=category)
        else:
            queryset = ReadyApiMedia.objects.all()
        return queryset

    def list(self, request):
        queryset = ReadyApiMedia.objects.all()
        serializer = ReadyApiMediaSerializer(queryset, many=True)
        response_data = {
            'readyApisMedia': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api media list.', response_data, status.HTTP_200_OK)


# Ready Api Category List
class ReadyApiCategoryList(ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = ReadyApiCategory.objects.all()
        serializer = ReadyApiCategorySerializer(queryset, many=True)
        response_data = {
            'readyApisCategory': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api categories list.', response_data, status.HTTP_200_OK)


# Ready Api Demo
@api_view(['POST'])
@permission_classes((AllowAny,))
def readyApiDemo(request):
    if request.method == 'POST':
        serializer = ReadyApiDemoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            apikey = settings.DEMO_API_KEY

            api = ReadyApis.objects.get(pk=serializer.data.get('api_id'))

            api_data = {
                'data': serializer.data.get('data')
            }

            data = json.dumps(api_data)

            headers = {
                'x-api-key': apikey,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            req = requests.post(
                api.cloud_url, data=data, headers=headers)

            response_data = {
                'demoData': req.json()
            }

            return response.MessageWithStatusSuccessAndData(True, 'Ready api demo.', response_data, status.HTTP_200_OK)
        else:
            return response.SerializerError(serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')

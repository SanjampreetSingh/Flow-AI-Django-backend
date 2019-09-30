import json
import requests

# Django Rest Framework Files
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# locals
from .imports import *


@api_view(['POST'])
@permission_classes((AllowAny,))
def packageReadyApiCallInference(request):
    if request.method == 'POST':
        serializer = InferenceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            apikey = request.data.get('api_key')

            api = ReadyApis.objects.filter(
                reference_url=request.data.get('api_name'))

            api_data = {
                'data': request.data.get('data')
            }

            data = json.dumps(api_data)

            headers = {
                'x-api-key': apikey,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            req = requests.post(
                api[0].cloud_url, data=data, headers=headers)

            inference_response = {
                'demoData': req.json()
            }

            return response.MessageWithStatusSuccessAndData(True, 'Ready api demo.', inference_response, status.HTTP_200_OK)
        else:
            return response.SerializerError(serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')


@api_view(['POST'])
@permission_classes((AllowAny,))
def validateApiKey(request):
    if request.method == 'POST':
        serializer = ApiKeySerializer(data=request.data)
        if serializer.is_valid():
            app = Apps.objects.filter(
                apikey_value=request.data.get('api_key'))

            if app.count() == 0:
                return response.Error400WithMessage('Invalid api key.')
            else:
                return response.MessageWithStatusAndSuccess(True, 'Api key is valid.', status.HTTP_200_OK)
        else:
            return response.SerializerError(details=serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')


@api_view(['POST'])
@permission_classes((AllowAny,))
def activeApiList(request):
    if request.method == 'POST':
        serializer = ApiKeySerializer(data=request.data)
        if serializer.is_valid():
            active_models = {}
            try:
                app = Apps.objects.filter(
                    apikey_value=request.data.get('api_key'))
                active_models = {
                    'ready_apis': app[0].ready_apis
                }
            except:
                pass

            return response.MessageWithStatusSuccessAndData(True, 'Active Api List.', active_models, status.HTTP_200_OK)
        else:
            return response.SerializerError(details=serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')

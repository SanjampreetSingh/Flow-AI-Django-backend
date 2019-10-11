import json
import requests
import threading

# Django Rest Framework Files
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# locals
from .imports import *
from readyApiUsages.views import (
    increase_ready_call
)


@api_view(['POST'])
@permission_classes((AllowAny,))
def packageReadyApiCallInference(request):
    if request.method == 'POST':
        serializer = InferenceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            api_key = request.data.get('api_key')
            app = (Apps.objects.filter(apikey_value=api_key))[0]
            ready_usage_bucket = ReadyApiUsageBuckets.objects.get(app=app)
            if app.active is not False and ready_usage_bucket.active is not False:
                api = (ReadyApis.objects.filter(
                    reference_url=request.data.get('api_name')))[0]

                api_data = {
                    'data': request.data.get('data')
                }

                data = json.dumps(api_data)

                headers = {
                    'x-api-key': api_key,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                req = requests.post(
                    api.cloud_url, data=data, headers=headers)

                inference_response = {
                    'demoData': req.json()
                }

                increase_calls = threading.Thread(
                    target=increase_ready_call,
                    args=(api_key,)
                )
                increase_calls.daemon = True
                increase_calls.start()

                return response.MessageWithStatusSuccessAndData(True, 'Ready api demo.', inference_response, status.HTTP_200_OK)
            else:
                return response.Error400WithMessage('Api key inactive or Usage qouta is full.')
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
                return response.Error400WithMessage('Invalid api key.')

            return response.MessageWithStatusSuccessAndData(True, 'Active Api List.', active_models, status.HTTP_200_OK)
        else:
            return response.SerializerError(details=serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')

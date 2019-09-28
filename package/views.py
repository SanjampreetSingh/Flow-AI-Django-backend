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
                reference_api_call=request.data.get('api_name'))

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

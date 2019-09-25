import json
import requests
# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from users.models import (Users)
# from readyApis.models import (ReadyApis)
from .models import (Apps)
from .serializer import (
    AppWriteSerializer,
    AppReadSerializer
)
from comman.boto import(
    boto_create_api_key,
)
from comman.permissions import(
    HasVerifiedEmail
)
from comman import response


class Apps(viewsets.ModelViewSet):
    queryset = Apps.objects.all()
    permission_classes = [IsAuthenticated, HasVerifiedEmail]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppWriteSerializer
        return AppReadSerializer

    def list(self, request):
        if request.method == 'GET':
            try:
                applications = Apps.objects.filter(user=request.user.id)
            except Apps.DoesNotExist:
                return response.MessageWithStatusAndSuccess(False, 'Application not found.', status.HTTP_404_NOT_FOUND)

            serializer = get_serializer_class(applications, many=True)

            response_data = {
                'application': serializer.data
            }
            return response.MessageWithStatusSuccessAndData(True, 'Application data.', response_data, status.HTTP_200_OK)
        else:
            return response.Error400WithMessage('Bad Request.')

    def create(self, request):
        if request.method == 'POST':
            serializer = get_serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                serializer.validated_data['active'] = True
                app = serializer.save()

                create_api_key = boto_create_api_key(
                    request.data.get('name'), True, True, str(app.id))

                Apps.objects.filter(id=app.id).update(
                    apikey_value=create_api_key.get('value'),
                    apikey_id=create_api_key.get('id'),
                )

                return response.MessageWithStatusAndSuccess(True, 'App created successfully.', status.HTTP_201_CREATED)

            else:
                return response.SerializerError(serializer.errors)
        else:
            return response.Error400WithMessage('Bad Request.')


# class ReadyAppImageViewSet(viewsets.ModelViewSet):
#     queryset = ReadyAppImage.objects.all()
#     serializer_class = ReadyAppImageSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JSONWebTokenAuthentication]
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
from readyApis.models import (ReadyApis)
from .models import (Apps)
from .serializer import (
    AppWriteSerializer,
    AppReadSerializer,
    AppActivateReadyApisSerializer
)
from comman.boto import(
    boto_create_api_key,
    boto_create_usage_plan_key
)
from comman.permissions import(
    HasVerifiedEmail
)
from comman import response


class AppsView(viewsets.ModelViewSet):
    queryset = Apps.objects.all()
    permission_classes = [IsAuthenticated, HasVerifiedEmail]
    authentication_classes = [JSONWebTokenAuthentication]
    lookup_field = 'reference_url'

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

            serializer = AppReadSerializer(applications, many=True)

            response_data = {
                'application': serializer.data
            }
            return response.MessageWithStatusSuccessAndData(True, 'Application data.', response_data, status.HTTP_200_OK)
        else:
            return response.Error400WithMessage('Bad Request.')

    def create(self, request):
        if request.method == 'POST':
            reference_url = request.data.get('reference_url')
            if Apps.objects.filter(reference_url=reference_url, user_id=request.user).exists() is not True:
                serializer = AppWriteSerializer(data=request.data)
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
                return response.Error400WithMessage('User cannot create different applications with same name.')
        else:
            return response.Error400WithMessage('Bad Request.')

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# class ReadyAppImageViewSet(viewsets.ModelViewSet):
#     queryset = ReadyAppImage.objects.all()
#     serializer_class = ReadyAppImageSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JSONWebTokenAuthentication]


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def addReadyApiToUsagePlan(request):
    """
    API_KEY from create_api_key() and returns apikey_id, which is saved in App Model.
    USAGE_PLAN of  READY API is made on Console_AWS and usagePlanId is stored in ReadyApi Model.
    create_usage_plan_key() is used for adding an existing API key to a usage plan.
    ACTIVE_APIS[] is updated with activated API Name's
    """
    if request.method == 'POST':
        serializer = AppActivateReadyApisSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            app = Apps.objects.filter(
                reference_url=serializer.data.get('app_reference_url'))
            api = ReadyApis.objects.filter(pk=serializer.data.get('api_id'))

            if app[0].active_apis is None:
                listOfApis = []
            else:
                listOfApis = app[0].active_apis

            if api[0].name not in listOfApis:
                listOfApis.append(api[0].name)
            else:
                action = None

            create_usage_plan_key = boto_create_usage_plan_key(
                api[0].usage_plan_id,
                app[0].apikey_id,
                'API_KEY'
            )

            app.update(active_apis=listOfApis)

            return response.MessageWithStatusAndSuccess(True, 'Api added to app.', status.HTTP_200_OK)
        else:
            return response.SerializerError(serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')

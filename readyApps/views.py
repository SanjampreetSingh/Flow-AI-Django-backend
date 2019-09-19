import pprint
# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

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
from .models import (ReadyApps, ReadyAppImage)
from .serializer import (
    ReadyAppWriteSerializer,
    ReadyAppReadSerializer,
    ReadyAppImageSerializer)
from comman.boto import(
    boto_create_api_key,
    boto_create_usage_plan,
    boto_create_usage_plan_key,
    boto_update_usage_plan,
)


class ReadyAppViewSet(viewsets.ModelViewSet):
    queryset = ReadyApps.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReadyAppWriteSerializer
        return ReadyAppReadSerializer

    def list(self, request):
        if request.method == 'GET':
            try:
                applications = ReadyApps.objects.filter(user=request.user.id)
            except ReadyApps.DoesNotExist:
                return Response(
                    {
                        'success': False,
                        'message': 'Application not found.',
                    },
                    status=status.HTTP_404_NOT_FOUND)

            serializer = ReadyAppReadSerializer(applications, many=True)
            return Response(
                {
                    'success': True,
                    'message': 'Application data.',
                    'data':
                    {
                        'application': serializer.data
                    }
                },
                status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'success': False,
                    'message': 'Bad Request.'
                },
                status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        if request.method == 'POST':
            # query = UserSubscription.objects.get(user=request.user.id)
            serializer = ReadyAppWriteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                app = serializer.save()

                create_api_key = boto_create_api_key(
                    request.data.get('name'), True, True, str(app.id))

                # query.plan.burst_limit, query.plan.rate_limit, query.plan.quota_limit,

                create_usage_plan = boto_create_usage_plan(
                    request.data.get('name'))

                api_create_usage_plan_key = boto_create_usage_plan_key(
                    create_usage_plan.get('id'), create_api_key.get('id'), 'API_KEY')

                ReadyApps.objects.filter(id=app.id).update(
                    apikey_value=create_api_key.get('value'),
                    apikey_id=create_api_key.get('id'),
                    usage_plan_id=create_usage_plan.get('id')
                )

                return Response(
                    {
                        'success': True,
                        'message': 'App created successfully.',
                    },
                    status=status.HTTP_201_CREATED
                )

            else:
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid data.',
                        'error':
                        {
                            'details': serializer.errors
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST)


class ReadyAppImageViewSet(viewsets.ModelViewSet):
    queryset = ReadyAppImage.objects.all()
    serializer_class = ReadyAppImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


# Activate Api Usage Plan
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def activateApiUsagePlan(request):
    if request.method == 'POST':

        app = ReadyApps.objects.filter(
            id=request.data.get('app_id')).values('usage_plan_id')

        api = ReadyApis.objects.filter(
            id=request.data.get('api_id')).values('apikey_stage')

        pprint((api[0].get('apikey_stage')))

        update_usage_plan = boto_update_usage_plan(
            app[0].get('usage_plan_id'),
            "add",
            "/apiStages",
            api[0].get('apikey_stage')
        )

        return Response(
            {
                'success': True,
                'message': 'Api added to app.'
            },
            status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'success': False,
                'message': 'Bad Request.'
            },
            status=status.HTTP_400_BAD_REQUEST)


# Deactivate Api Usage Plan
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def deactivateApiUsagePlan(request):
    if request.method == 'POST':

        app = ReadyApps.objects.filter(
            id=request.data.get('app_id')).values('usage_plan_id')

        api = ReadyApis.objects.filter(
            id=request.data.get('api_id')).values('apikey_stage')

        pprint((api[0].get('apikey_stage')))

        update_usage_plan = boto_update_usage_plan(
            app[0].get('usage_plan_id'),
            "remove",
            "/apiStages",
            api[0].get('apikey_stage')
        )

        return Response(
            {
                'success': True,
                'message': 'Api removed from app.'
            },
            status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'success': False,
                'message': 'Bad Request.'
            },
            status=status.HTTP_400_BAD_REQUEST)

import boto3
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
from .models import (ReadyApps, ReadyAppImage)
from .serializer import (ReadyAppSerializer, ReadyAppImageSerializer)


# Boto3 Connection Variable
client = boto3.client(
    'apigateway',
    region_name='us-east-2',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


class ReadyAppViewSet(viewsets.ModelViewSet):
    queryset = ReadyApps.objects.all()
    serializer_class = ReadyAppSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

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

            serializer = ReadyAppSerializer(applications, many=True)
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
            serializer = ReadyAppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                app = serializer.save()

                boto_create_api_key = boto_create_api_key(
                    request.data.get('name'), True, True, str(app.id))

                # query.plan.burst_limit, query.plan.rate_limit, query.plan.quota_limit,

                boto_create_usage_plan = boto_create_usage_plan(
                    request.data.get('name'))

                boto_api_create_usage_plan_key = boto_create_usage_plan_key(
                    boto_create_usage_plan.get('id'), boto_create_api_key.get('id'), 'API_KEY')

                ReadyApps.objects.filter(id=app.id).update(
                    apikey_value=boto_create_api_key.get('value'),
                    apikey_id=boto_create_api_key.get('id'),
                    usage_plan_id=boto_create_usage_plan.get('id')
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
                            'details': str(serializer.errors)
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST)


def boto_create_api_key(name: str, enabled: bool, generateDistinctId: bool, customerId: str):
    return client.create_api_key(
        name=name,
        enabled=enabled,
        generateDistinctId=generateDistinctId,
        customerId=customerId
    )


def boto_create_usage_plan(name: str):
    return client.create_usage_plan(
        name=name,
        throttle={
            'burstLimit': 10,
            'rateLimit': 10
        },
        quota={
            'limit': 100,
            'period': 'MONTH'
        },
    )


def boto_create_usage_plan_key(usagePlanId, keyId, keyType: str):
    return client.create_usage_plan_key(
        usagePlanId=usagePlanId,
        keyId=keyId,
        keyType=keyType
    )


# some comment
class ReadyAppImageViewSet(viewsets.ModelViewSet):
    queryset = ReadyAppImage.objects.all()
    serializer_class = ReadyAppImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

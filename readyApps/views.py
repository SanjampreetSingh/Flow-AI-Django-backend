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
client = boto3.client('apigateway', region_name='us-east-2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


class ReadyAppViewSet(viewsets.ModelViewSet):
    queryset = ReadyApps.objects.all()
    serializer_class = ReadyAppSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def create(self, request):
        if request.method == 'POST':
            # query = UserSubscription.objects.get(user=request.user.id)
            serializer = ReadyAppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                app = serializer.save()
                api_create_api_key = client.create_api_key(
                    name=request.data.get('name'),
                    enabled=True,
                    generateDistinctId=True,
                    customerId=str(app.id)
                )
                # query.plan.burst_limit,
                # query.plan.rate_limit
                # query.plan.quota_limit,
                api_create_usage_plan = client.create_usage_plan(
                    name=request.data.get('name'),
                    throttle={
                        'burstLimit': 10,
                        'rateLimit': 10
                    },
                    quota={
                        'limit': 100,
                        'period': 'MONTH'
                    },
                )
                api_create_usage_plan_key = client.create_usage_plan_key(
                    usagePlanId=api_create_usage_plan.get('id'),
                    keyId=api_create_api_key.get('id'),
                    keyType='API_KEY'
                )
                ReadyApps.objects.filter(id=app.id).update(apikey_value=api_create_api_key.get('value'),
                                                           apikey_id=api_create_api_key.get(
                    'id'),
                    usage_plan_id=api_create_usage_plan.get('id'))
                return Response({'success': True,
                                 'message': 'Data Added',
                                 'data': serializer.data,
                                 'api_create_api_key': api_create_api_key,
                                 'api_create_usage_plan': api_create_usage_plan,
                                 'api_create_usage_plan_key': api_create_usage_plan_key},
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadyAppImageViewSet(viewsets.ModelViewSet):
    queryset = ReadyAppImage.objects.all()
    serializer_class = ReadyAppImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

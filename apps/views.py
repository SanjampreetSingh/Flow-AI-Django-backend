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
from .models import (Apps, AppImage)
from .serializer import (AppSerializer, AppImageSerializer)


class AppViewSet(viewsets.ModelViewSet):
    queryset = Apps.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


# def applicationCreateAPI(request):
#     if request.method == 'POST':
#         query = UserSubscription.objects.get(user=request.user.id)
#         serializer = UserAppSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['user'] = request.user
#             app = serializer.save()
#             api_create_api_key = client.create_api_key(
#                 name=request.data.get('name'),
#                 enabled=True,
#                 generateDistinctId=True,
#                 customerId=str(app.id)
#             )
#             api_create_usage_plan = client.create_usage_plan(
#                 name=request.data.get('name'),
#                 throttle={
#                     'burstLimit': query.plan.burst_limit,
#                     'rateLimit': query.plan.rate_limit
#                 },
#                 quota={
#                     'limit': query.plan.quota_limit,
#                     'period': 'MONTH'
#                 },
#             )
#             api_create_usage_plan_key = client.create_usage_plan_key(
#                 usagePlanId=api_create_usage_plan.get('id'),
#                 keyId=api_create_api_key.get('id'),
#                 keyType='API_KEY'
#             )
#             UserApp.objects.filter(id=app.id).update(apikey_value=api_create_api_key.get('value'),
#                                                      apikey_id=api_create_api_key.get(
#                                                      'id'),
#                                                      usage_plan_id=api_create_usage_plan.get('id'))
#             return Response({'success': True,
#                              'message': 'Data Added',
#                              'data': serializer.data,
#                              'api_create_api_key': api_create_api_key,
#                              'api_create_usage_plan': api_create_usage_plan,
#                              'api_create_usage_plan_key': api_create_usage_plan_key},
#                             status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppImageViewSet(viewsets.ModelViewSet):
    queryset = AppImage.objects.all()
    serializer_class = AppImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

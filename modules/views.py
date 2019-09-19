# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from .models import (Modules)
from .serializer import (ModuleSerializer)


# Module's List
class ModuleList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Modules.objects.all()
    serializer_class = ModuleSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ModuleSerializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'message': 'Module list.',
                'data': {
                    'module': serializer.data
                }
            },
            status=status.HTTP_200_OK)


# Module's Details
class ModuleDetails(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Modules.objects.all()
    lookup_field = 'reference_url'
    serializer_class = ModuleSerializer

    def retrieve(self, request):
        queryset = self.get_queryset()
        serializer = ModuleSerializer(queryset)
        return Response(
            {
                'success': True,
                'message': 'Module details.',
                'data': {
                    'readyApisMedia': serializer.data
                }
            },
            status=status.HTTP_200_OK)

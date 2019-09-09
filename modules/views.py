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


# Api Category List
class ModuleList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Modules.objects.all()
    serializer_class = ModuleSerializer


class ModuleDetails(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Modules.objects.all()
    serializer_class = ModuleSerializer

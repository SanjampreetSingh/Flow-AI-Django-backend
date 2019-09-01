from datetime import datetime

# Django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from users.models import (Users)
from .models import (Plans)
from .serializer import (PlanSerializer)


# Plan List
class PlanListUser(ListAPIView):
    permission_classes = (IsAuthenticated)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Plans.objects.all()
    serializer_class = PlanSerializer


class PlanListFrontend(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Plans.objects.all()
    serializer_class = PlanSerializer

# Django Rest Framework Files
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from .models import (Modules)
from .serializer import (ModuleSerializer)
from comman import response


# Module's List
class ModuleList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request):
        queryset = Modules.objects.all()
        serializer = ModuleSerializer(queryset, many=True)
        response_data = {
            'modules': serializer.data
        }
        return response.MessageWithStatusAndSuccess(True, 'Module list.', response_data, status.HTTP_200_OK)


# Module's Details
class ModuleDetails(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    lookup_field = 'reference_url'

    def retrieve(self, request, reference_url):
        queryset = Modules.objects.all()
        serializer = ModuleSerializer(queryset, many=True)
        response_data = {
            'module': serializer.data[0]
        }
        return response.MessageWithStatusAndSuccess(True, 'Module details.', response_data, status.HTTP_200_OK)

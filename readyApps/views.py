# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from readyApis.models import (ReadyApis)
from apps.models import (Apps)
from readyApiUsages.models import (ReadyApiUsageBuckets)
from .serializer import (
    AppActivateReadyAppsSerializer
)
from comman.boto import (
    boto_create_usage_plan_key
)
from comman.permissions import (
    HasVerifiedEmail
)
from comman import response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def addReadyApiToApp(request):
    """
    API_KEY from create_api_key() and returns apikey_id, which is saved in App Model.
    USAGE_PLAN of  READY API is made on Console_AWS and usagePlanId is stored in ReadyApi Model.
    create_usage_plan_key() is used for adding an existing API key to a usage plan.
    ACTIVE_APIS[] is updated with activated API Name's
    """
    if request.method == 'POST':
        serializer = AppActivateReadyAppsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            app = Apps.objects.filter(
                reference_url=serializer.data.get('app_reference_url'))
            api = ReadyApis.objects.filter(pk=serializer.data.get('api_id'))
            ReadyApiUsageBuckets.objects.filter(app=app[0]).update(active=True)

            if app[0].ready_apis is None:
                listOfApis = []
            else:
                listOfApis = app[0].ready_apis

            if api[0].name not in listOfApis:
                listOfApis.append(api[0].name)
            else:
                action = None

            if app[0].usage_plans is None:
                listUsagePlan = []
            else:
                listUsagePlan = app[0].usage_plans

            if api[0].usage_plan_id not in listUsagePlan:
                listUsagePlan.append(api[0].usage_plan_id)
            else:
                action = None

            create_usage_plan_key = boto_create_usage_plan_key(
                api[0].usage_plan_id,
                app[0].apikey_id,
                'API_KEY'
            )

            app.update(ready_apis=listOfApis, usage_plans=listUsagePlan)

            return response.MessageWithStatusAndSuccess(True, 'Api added to app.', status.HTTP_200_OK)
        else:
            return response.SerializerError(serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')

from rest_framework import status
# Local
from .models import (ReadyApiUsagePerModels)
from .serializer import (
    ReadyApiUsagePerModelsReadSerializer,
    ReadyApiUsagePerModelsWriteSerializer
)
from apps.models import (
    Apps
)
from readyApis.models import (
    ReadyApis
)

# from comman.boto import()
from comman import response


def increase_ready_usage_per_model_call(app_id, api_id):
    app = (Apps.objects.get(pk=app_id))
    api = (ReadyApis.objects.get(pk=api_id))
    ready_usage_per_model = (
        ReadyApiUsagePerModels.objects.get_or_create(app=app, api=api))[0]
    ready_usage_per_model.usage += 1
    ready_usage_per_model.save()
    return response.MessageWithStatusAndSuccess(True, 'Call made successfully.', status.HTTP_200_OK)

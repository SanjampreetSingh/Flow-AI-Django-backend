from rest_framework import serializers
from . import models


# App Activate ReadyApps Serializer
class AppActivateReadyAppsSerializer(serializers.Serializer):
    """
    Serializer which accepts app_reference_url and api_id.
    Used to link app with Ready API's.
    """
    app_reference_url = serializers.CharField(required=True)
    api_id = serializers.IntegerField(required=True)

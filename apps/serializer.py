from rest_framework import serializers
from . import models


# Apps Write Serializers
class AppWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = "__all__"
        lookup_field = 'reference_url'
        extra_kwargs = {
            'url': {'lookup_field': 'reference_url'}
        }


# Apps Read Serializers
class AppReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = [
            'id', 'user', 'name', 'description', 'apikey_value', 'reference_url', 'active_apis'
        ]
        lookup_field = 'reference_url'
        extra_kwargs = {
            'url': {'lookup_field': 'reference_url'}
        }


# # AppImage Serializer
# class AppImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.AppImage
#         fields = "__all__"


class AppActivateReadyApisSerializer(serializers.Serializer):
    """
    Serializer which accepts app_id and api_id.
    Used to link app with Ready API's. 
    """
    app_id = serializers.IntegerField(required=True)
    api_id = serializers.IntegerField(required=True)

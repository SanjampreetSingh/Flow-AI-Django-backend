from rest_framework import serializers
from . import models


# Apps Write Serializers
class AppWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = "__all__"


# Apps Read Serializers
class AppReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = [
            'id', 'user', 'name', 'description', 'apikey_value', 'reference_url', 'ready_apis'
        ]


# # AppImage Serializer
# class AppImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.AppImage
#         fields = "__all__"

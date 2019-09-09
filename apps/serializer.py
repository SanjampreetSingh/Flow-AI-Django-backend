from rest_framework import serializers
from . import models


# Apps Serializer
class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apps
        fields = "__all__"


# Apps Serializer
class AppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppImage
        fields = "__all__"

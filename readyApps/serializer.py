from rest_framework import serializers
from . import models


# ReadyApps Serializer
class ReadyAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApps
        fields = "__all__"


# ReadyAppImage Serializer
class ReadyAppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyAppImage
        fields = "__all__"

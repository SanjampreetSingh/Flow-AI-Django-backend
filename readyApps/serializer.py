from rest_framework import serializers
from . import models


# ReadyApps Write Serializers
class ReadyAppWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApps
        fields = "__all__"


# ReadyApps Read Serializers
class ReadyAppReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApps
        fields = [
            'id', 'user', 'name', 'description', 'apikey_value', 'reference_url', 'ready_apis'
        ]


# ReadyAppImage Serializer
class ReadyAppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyAppImage
        fields = "__all__"

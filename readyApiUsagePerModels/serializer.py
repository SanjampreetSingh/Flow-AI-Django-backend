from rest_framework import serializers
from . import models


# Ready Api Usage Per Models Write Serializers
class ReadyApiUsagePerModelsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiUsagePerModels
        fields = "__all__"


# Ready Api Per Models Read Serializers
class ReadyApiUsagePerModelsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiUsagePerModels
        fields = [
            'api', 'app', 'usage',
        ]

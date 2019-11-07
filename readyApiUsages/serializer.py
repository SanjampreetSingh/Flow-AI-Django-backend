from rest_framework import serializers
from . import models


# Ready Api Usage Buckets Write Serializers
class ReadyApiUsageBucketsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiUsageBuckets
        fields = "__all__"


# Ready Api Usage Buckets Read Serializers
class ReadyApiUsageBucketsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiUsageBuckets
        fields = [
            'bucket', 'usage', 'threshold',
        ]

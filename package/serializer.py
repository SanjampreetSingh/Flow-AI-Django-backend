# Django Rest Framework Files
from rest_framework import serializers

# locals
from . import imports


# Api Key Serializers
class ApiKeySerializer(serializers.Serializer):
    api_key = serializers.CharField(required=True)


# Inference Serializers
class InferenceSerializer(serializers.Serializer):
    api_name = serializers.CharField(required=True)
    api_key = serializers.CharField(required=True)
    # data = serializers.CharField()

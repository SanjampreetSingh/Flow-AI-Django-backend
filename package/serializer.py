# Django Rest Framework Files
from rest_framework import serializers

# locals
from . import imports


# Inference Serializers
class InferenceSerializer(serializers.Serializer):
    api_name = serializers.CharField(required=True)
    api_key = serializers.CharField(required=True)
    data = serializers.CharField()


# Inference Serializers
class InferenceSerializer(serializers.Serializer):
    api_name = serializers.CharField(required=True)
    api_key = serializers.CharField(required=True)
    data = serializers.CharField()

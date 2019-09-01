from rest_framework import serializers
from . import models


# API Category Serializer
class ApiCategorySerializer(ModelSerializer):
    class Meta:
        model = models.ApiCategory
        fields = "__all__"


# Api Serializer
class ApiSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.Api
        fields = "__all__"


# Api Image Serializer
class ApiImageSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.ApiImage
        fields = "__all__"

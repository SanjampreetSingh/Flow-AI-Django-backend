from rest_framework import serializers
from . import models


# Ready API Category Serializer
class ReadyApiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiCategory
        fields = ['id', 'name']


# Ready Api Serializer
class ReadyApiSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.ReadyApis
        fields = ['name', 'category', 'active', 'tagline', 'description', 'image_url',
                  'use_cases', 'recommendations', 'price', 'tag', 'reference_url']


# Ready Api Media Serializer
class ReadyApiMediaSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.ReadyApiMedia
        fields = ['category', 'media', 'url']


# Ready Api Demo Serializers
class ReadyApiDemoSerializer(serializers.Serializer):
    """
    Serializer which accepts api_id and data.
    """

    api_id = serializers.IntegerField(required=True)
    data = serializers.CharField()

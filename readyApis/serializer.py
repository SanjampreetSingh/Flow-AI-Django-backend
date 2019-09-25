from rest_framework import serializers
from . import models


# Ready API Category Serializer
class ReadyApiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApiCategory
        fields = "__all__"


# Ready Api Serializer
class ReadyApiSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.ReadyApis
        fields = "__all__"


# Ready Api Media Serializer
class ReadyApiMediaSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = models.ReadyApiMedia
        fields = "__all__"


# Ready Api Demo Serializers
class ReadyApiDemoSerializer(serializers.Serializer):
    """
    Serializer which accepts api_id and data.
    """

    api_id = serializers.IntegerField(required=True)
    data = serializers.CharField()

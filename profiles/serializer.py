from rest_framework import serializers
from . import models


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='email')

    class Meta:
        model = models.Profiles
        fields = "__all__"


# Profile Picture Serializer
class ProfilePictureSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='email')

    class Meta:
        model = models.ProfilePicture
        fields = "__all__"

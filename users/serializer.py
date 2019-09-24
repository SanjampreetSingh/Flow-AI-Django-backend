from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from . import models

UserModel = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, validators=[
                                   validators.UniqueValidator(queryset=models.Users.objects.all())])
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = models.Users
        fields = "__all__"


# Serializer which accepts an OAuth2 access token and provider.
class SocialSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)


# Serializer which accepts an email.
class CheckUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

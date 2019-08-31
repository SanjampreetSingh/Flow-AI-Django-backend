from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

UserModel = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = models.Users
        fields = ('user_type', 'email', 'password',
                  'active', 'verified', 'complete', 'steps')

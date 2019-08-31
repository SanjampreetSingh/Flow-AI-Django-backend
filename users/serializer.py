from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

UserModel = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ('email', 'user_type', 'password',
                  'active', 'verified', 'complete', 'steps')
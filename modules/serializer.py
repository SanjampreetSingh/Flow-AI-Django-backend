from rest_framework import serializers
from . import models


# Module Serializer
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Modules
        fields = "__all__"

from rest_framework import serializers
from . import models


# Plan Serializer
class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Plans
        fields = "__all__"

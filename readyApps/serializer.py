from rest_framework import serializers
from . import models


# ReadyApps Write Serializers
class ReadyAppWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApps
        fields = "__all__"


# ReadyApps Read Serializers
class ReadyAppReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyApps
        fields = [
            'id', 'user', 'name', 'description', 'apikey_value', 'reference_url', 'ready_apis'
        ]


# ReadyAppImage Serializer
class ReadyAppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadyAppImage
        fields = "__all__"


# Ready DeActivate Serializers
class ReadyActionsSerializer(serializers.Serializer):
    """
    Serializer which accepts app_id, api_id and action.
    """
    ACTION_CHOICES = (
        ('A'),
        ('R'),
    )

    app_id = serializers.IntegerField(required=True)
    api_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=ACTION_CHOICES, required=True)


# Ready Api Demo Serializers
class ReadyApiDemoSerializer(serializers.Serializer):
    """
    Serializer which accepts api_id.
    """

    api_name = serializers.CharField(required=True)
    apikey = serializers.CharField(required=True)
    data = serializers.CharField()

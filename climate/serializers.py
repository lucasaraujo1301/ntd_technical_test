from rest_framework import serializers

from core.models import Climate


class ClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climate
        fields = ["id", "name"]

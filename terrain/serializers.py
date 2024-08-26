from rest_framework import serializers

from core.models import Terrain


class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = ["id", "name"]

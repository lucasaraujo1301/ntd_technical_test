from rest_framework import serializers

from core import models


class PlanetSerializer(serializers.ModelSerializer):
    terrains = serializers.SlugRelatedField(
        queryset=models.Terrain.objects.all(),
        many=True,
        required=False,
        slug_field="name",
    )
    climates = serializers.SlugRelatedField(
        queryset=models.Climate.objects.all(),
        many=True,
        required=False,
        slug_field="name",
    )

    class Meta:
        model = models.Planet
        fields = ["id", "name", "population", "terrains", "climates"]

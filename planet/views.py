from rest_framework import viewsets, permissions

from core.models import Planet
from planet.serializers import PlanetSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    serializer_class = PlanetSerializer
    queryset = Planet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

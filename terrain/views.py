from rest_framework import viewsets, permissions

from core.models import Terrain
from terrain.serializers import TerrainSerializer


class TerrainViewSet(viewsets.ModelViewSet):
    serializer_class = TerrainSerializer
    queryset = Terrain.objects.all()
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import viewsets, permissions

from core.models import Climate
from climate.serializers import ClimateSerializer


class ClimateViewSet(viewsets.ModelViewSet):
    serializer_class = ClimateSerializer
    queryset = Climate.objects.all()
    permission_classes = [permissions.IsAuthenticated]

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Terrain
from user.tests.test_user_api import create_user

CREATE_GET_TERRAINS_URL = reverse("terrain:terrain-list")


def create_terrain(**params):
    return Terrain.objects.create(**params)


class PublicTerrainsApiTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()

    def test_create_terrains_unauthorized(self):
        data = {"name": "test"}
        res = self.client_api.post(CREATE_GET_TERRAINS_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )

    def test_get_terrains_unauthorized(self):
        res = self.client_api.get(CREATE_GET_TERRAINS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )


class PrivateProductApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@example.com", password="testpass123", name="Test Name"
        )

        data = {"name": "test"}
        self.terrain = create_terrain(**data)

        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)

    def test_create_terrain_success(self):
        data = {"name": "deserts"}

        res = self.client_api.post(CREATE_GET_TERRAINS_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], data["name"])

    def test_create_terrain_unsuccessful(self):
        data = {"name": "test"}

        res = self.client_api.post(CREATE_GET_TERRAINS_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(res.data["name"][0]), "terrain with this name already exists."
        )

    def test_get_terrain(self):
        res = self.client_api.get(CREATE_GET_TERRAINS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], self.terrain.id)

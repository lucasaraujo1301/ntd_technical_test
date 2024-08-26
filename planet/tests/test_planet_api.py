from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from climate.tests.test_climate_api import create_climate
from core.models import Planet
from terrain.tests.test_terrain_api import create_terrain
from user.tests.test_user_api import create_user

CREATE_GET_PLANET_URL = reverse("planet:planet-list")


def create_planet(**params):
    return Planet.objects.create(**params)


class PublicPlanetsApiTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()

    def test_create_planets_unauthorized(self):
        data = {"name": "test"}
        res = self.client_api.post(CREATE_GET_PLANET_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )

    def test_get_planets_unauthorized(self):
        res = self.client_api.get(CREATE_GET_PLANET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            "Authentication credentials were not provided.", res.data["detail"]
        )


class PrivateProductApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@example.com", password="testpass123", name="Test Name"
        )

        data = {"name": "test", "population": 2000}
        self.planet = create_planet(**data)
        self.terrain = create_terrain(name="deserts")
        self.climate = create_climate(name="arid")

        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)

    def test_create_planet_success(self):
        data = {"name": "Tatooine", "population": 4000}

        res = self.client_api.post(CREATE_GET_PLANET_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], data["name"])
        self.assertEqual(res.data["population"], data["population"])

    def test_create_planet_with_terrain_and_climate_success(self):
        data = {
            "name": "Tatooine",
            "population": 4000,
            "climates": [self.climate.name],
            "terrains": [self.terrain.name],
        }

        res = self.client_api.post(CREATE_GET_PLANET_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], data["name"])
        self.assertEqual(res.data["population"], data["population"])
        self.assertIn(self.climate.name, res.data["climates"])
        self.assertIn(self.terrain.name, res.data["terrains"])

    def test_create_planet_with_terrain_or_climate_wrong(self):
        data = {"name": "Tatooine", "population": 4000, "climates": ["test"]}

        res = self.client_api.post(CREATE_GET_PLANET_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["climates"][0], "Object with name=test does not exist."
        )

    def test_create_planet_unsuccessful(self):
        data = {"name": "test", "population": 2000}

        res = self.client_api.post(CREATE_GET_PLANET_URL, data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(res.data["name"][0]), "planet with this name already exists."
        )

    def test_get_planet(self):
        res = self.client_api.get(CREATE_GET_PLANET_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["id"], self.planet.id)

from typing import Union

import requests

from django.core.management.base import BaseCommand

from core import models


class Command(BaseCommand):
    """
    Django command to wait for database.
    """

    @property
    def graphql_url(self) -> str:
        return "https://swapi-graphql.netlify.app/.netlify/functions/index"

    @property
    def graphql_query(self) -> str:
        return "{allPlanets{planets{name population terrains climates}}}"

    def get_graphql_response(self) -> dict:
        response = requests.get(
            self.graphql_url, json={"query": self.graphql_query, "variables": {}}
        )
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(response.text))
            raise Exception("GraphQL query failed")
        return response.json()

    def get_planets_from_response(self, response) -> Union[dict, list]:
        return response.get("data", {}).get("allPlanets", {}).get("planets", [])

    def create_planet_data(self, name: str, population: int = None) -> models.Planets:
        """
        The create_planet_data function get or create the planet based on the graphql response.
        """
        return models.Planets.objects.get_or_create(name=name, population=population)

    def add_terrains_data(self, terrains: list) -> list[models.Terrain]:
        """
        The add_terrains_data function get or create the terrain based on the graphql response.
        """
        terrains_created = []
        for terrain in terrains:
            if terrain != "unknown":
                get, _ = models.Terrain.objects.get_or_create(name=terrain)
                terrains_created.append(get)

        return terrains_created

    def add_climates_data(self, climates: list) -> list[models.Climates]:
        """
        The add_climates_data function get or create the climates based on the graphql response.
        """
        climates_created = []
        for climate in climates:
            if climate != "unknown":
                get, _ = models.Climates.objects.get_or_create(name=climate)
                climates_created.append(get)

        return climates_created

    def add_climates_and_terrains_in_planets(
        self,
        planet: models.Planets,
        terrains: list[models.Terrain],
        climates: list[models.Climates],
    ):
        """
        The add_climates_and_terrains_in_planets function add terrain and climates in Planet instance
        """
        planet.terrains.add(*terrains)
        planet.climates.add(*climates)
        planet.save()

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write(f"Adding the base data from GraphQL API...")

        response = self.get_graphql_response()

        planets_data = self.get_planets_from_response(response)
        if not planets_data:
            return

        for planet_data in planets_data:
            terrains = self.add_terrains_data(planet_data.get("terrains"))
            climates = self.add_climates_data(planet_data.get("climates"))
            planet, _ = self.create_planet_data(
                planet_data.get("name"), planet_data.get("population")
            )
            self.add_climates_and_terrains_in_planets(planet, terrains, climates)

        self.stdout.write(self.style.SUCCESS("Done!"))

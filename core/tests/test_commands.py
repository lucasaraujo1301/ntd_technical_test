from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase, TestCase

from core import models


@patch("core.management.commands.wait_for_db.Command.check")
class TestWaitForDbCommand(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """
        The test_wait_for_db_ready function is a test case that checks whether the wait_for_db command works as
        expected.
        It does so by patching django.db.utils.ConnectionHandler._check_conn() and setting its return value to True,
        which simulates a successful database connection check.

        :param self: Access the instance of the class
        :param patched_check: Patch the check function
        :return: True
        :doc-author: Trelent
        """
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        The test_wait_for_db_delay function tests the wait_for_db command.
        It does this by patching the sleep function and check database functions,
        and then calling the wait_for_db command. It asserts that:
            - The patched check function was called 6 times (5 times for errors + 1 time for success)
            - The patched check function was called with 'default' as an argument

        :param self: Access the class instance
        :param patched_sleep: Mock the sleep function
        :param patched_check: Mock the check function
        :return: The number of times patched_check was called
        :doc-author: Trelent
        """
        patched_check.side_effect = (
            [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])


@patch("core.management.commands.add_base_planet_data.Command.get_graphql_response")
class TestAddBasePlanetDataCommand(TestCase):
    def test_add_base_planet_data(self, patched_get_graphql_response):
        patched_get_graphql_response.return_value = {
            "data": {
                "allPlanets": {
                    "planets": [
                        {
                            "name": "Tatooine",
                            "population": 200000,
                            "terrains": [
                                "desert"
                            ],
                            "climates": [
                                "arid"
                            ]
                        },
                    ]
                }
            }
        }

        call_command("add_base_planet_data")

        terrain = models.Terrain.objects.get(name="desert")
        climate = models.Climates.objects.get(name="arid")
        planet = models.Planets.objects.get(name="Tatooine")

        self.assertIsNotNone(terrain)
        self.assertIsNotNone(climate)
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "Tatooine")
        self.assertIn(terrain, planet.terrains.all())
        self.assertIn(climate, planet.climates.all())

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core import models


class AdminSiteTests(TestCase):
    def setUp(self):
        """
        The setUp function is run before every test in the class.
        It creates a new client, and then uses that client to log in as an admin user.
        The admin user is created using the create_superuser method of Django's built-in User model.

        :param self: Access the class variables and methods
        :return: Nothing
        :doc-author: Trelent
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )
        self.terrain = models.Terrain.objects.create(name="desert")
        self.climate = models.Climate.objects.create(name="arid")
        self.planet = models.Planet.objects.create(name="Tatooine", population=2000)
        self.planet.terrains.add(self.terrain)
        self.planet.climates.add(self.climate)

    def test_users_list(self):
        """
        The test_users_list function is a test case for the admin site.
        It checks that the user list view contains our created user's name and email address.

        :param self: Access the class attributes in the test_users_list function
        :return: The user's name and email
        :doc-author: Trelent
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """
        The test_edit_user_page function tests that the edit user page works.
        It does this by:
        - Getting the URL for editing a user (note that we are using the helper function reverse to build the URL since
            it will contain the URL to edit a user)
        - Making a GET request to that URL
        - Asserting that response gives back an HTTP 200 status code and contains both email and name of our test user

        :param self: Represent the instance of the class
        :return: A status code of 200 and the user's email and name
        :doc-author: Trelent
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_create_user_page(self):
        """
        The test_create_user_page function tests that the create user page works.
        It does this by:
            1. Getting the URL of the create user page (reverse)
            2. Making a GET request to it (client)
            3. Asserting that we use 200 as our response status code (status_code)
            4. Asserting that we have all input necessary to create an User

        :param self: Access the attributes and methods of the class in python
        :return: The status code, 200
        :doc-author: Trelent
        """
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="email"')
        self.assertContains(res, 'name="password1"')
        self.assertContains(res, 'name="password2"')
        self.assertContains(res, 'name="is_superuser"')
        self.assertContains(res, 'name="is_active"')
        self.assertContains(res, 'name="is_staff"')
        self.assertContains(res, 'name="name"')

    def test_terrain_list(self):
        """
        The test_terrain_list function is a test case for the admin site.
        It checks that the user list view contains our created terrain's name.

        :param self: Access the class attributes in the test_terrain_list function
        :return: The terrain's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_terrain_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.terrain.name)

    def test_edit_terrain_page(self):
        """
        The test_edit_terrain_page function tests that the edit user page works.
        It does this by:
        - Getting the URL for editing a terrain (note that we are using the helper function reverse to build the URL
            since it will contain the URL to edit a terrain)
        - Making a GET request to that URL
        - Asserting that response gives back an HTTP 200 status code and contains name of our test terrain

        :param self: Represent the instance of the class
        :return: A status code of 200 and the terrain's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_terrain_change", args=[self.terrain.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.terrain.name)

    def test_create_terrain_page(self):
        """
        The test_create_terrain_page function tests that the create terrain page works.
        It does this by:
            1. Getting the URL of the create terrain page (reverse)
            2. Making a GET request to it (client)
            3. Asserting that we use 200 as our response status code (status_code)
            4. Asserting that we have all input necessary to create an Terrain

        :param self: Access the attributes and methods of the class in python
        :return: The status code, 200
        :doc-author: Trelent
        """
        url = reverse("admin:core_terrain_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="name"')

    def test_climate_list(self):
        """
        The test_climate_list function is a test case for the admin site.
        It checks that the user list view contains our created climate's name.

        :param self: Access the class attributes in the test_climate_list function
        :return: The climate's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_climate_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.climate.name)

    def test_edit_climate_page(self):
        """
        The test_edit_climate_page function tests that the edit user page works.
        It does this by:
        - Getting the URL for editing a climate (note that we are using the helper function reverse to build the URL
            since it will contain the URL to edit a climate)
        - Making a GET request to that URL
        - Asserting that response gives back an HTTP 200 status code and contains name of our test climate

        :param self: Represent the instance of the class
        :return: A status code of 200 and the climate's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_climate_change", args=[self.climate.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.climate.name)

    def test_create_climate_page(self):
        """
        The test_create_climate_page function tests that the create climate page works.
        It does this by:
            1. Getting the URL of the create climate page (reverse)
            2. Making a GET request to it (client)
            3. Asserting that we use 200 as our response status code (status_code)
            4. Asserting that we have all input necessary to create an Climate

        :param self: Access the attributes and methods of the class in python
        :return: The status code, 200
        :doc-author: Trelent
        """
        url = reverse("admin:core_climate_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="name"')

    def test_planet_list(self):
        """
        The test_planet_list function is a test case for the admin site.
        It checks that the user list view contains our created planet's name.

        :param self: Access the class attributes in the test_planet_list function
        :return: The planet's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_planet_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.planet.name)

    def test_edit_planet_page(self):
        """
        The test_edit_planet_page function tests that the edit user page works.
        It does this by:
        - Getting the URL for editing a planet (note that we are using the helper function reverse to build the URL
            since it will contain the URL to edit a planet)
        - Making a GET request to that URL
        - Asserting that response gives back an HTTP 200 status code and contains name of our test planet

        :param self: Represent the instance of the class
        :return: A status code of 200 and the planet's name
        :doc-author: Trelent
        """
        url = reverse("admin:core_planet_change", args=[self.planet.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.planet.name)

    def test_create_planet_page(self):
        """
        The test_create_planet_page function tests that the create planet page works.
        It does this by:
            1. Getting the URL of the create climate page (reverse)
            2. Making a GET request to it (client)
            3. Asserting that we use 200 as our response status code (status_code)
            4. Asserting that we have all input necessary to create an Planet

        :param self: Access the attributes and methods of the class in python
        :return: The status code, 200
        :doc-author: Trelent
        """
        url = reverse("admin:core_planet_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="name"')
        self.assertContains(res, 'name="population"')
        self.assertContains(res, 'name="terrains"')
        self.assertContains(res, 'name="climates"')

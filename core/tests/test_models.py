from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        The test_create_user_with_email_successful function tests that creating a new user with an email is successful

        :param self: Represent the instance of the class
        :return: A user object
        """
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        The test_new_user_email_normalized function tests that the email address is normalized before saving it to
        the database.
        The test_new_user_email_normalized function creates a list of sample emails and their expected normalized
        versions.
        It then loops through each sample email, creating a user with that email address, and asserts that the user's
        actual email matches its expected normalized version.

        :param self: Access the attributes and methods of the class in python
        :return: A list of tuples
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(expected, user.email)

    def test_new_user_without_email_raises_error(self):
        """
        The test_new_user_without_email_raises_error function tests that a new user without an email address raises
        an error.

        :param self: Represent the instance of the class
        :return: An error if the email is not provided
        """

        with self.assertRaises(ValueError) as cm:
            get_user_model().objects.create_user("", "sample123")

        exception = cm.exception
        self.assertEqual(str(exception), "Email must be provided.")

    def test_new_user_with_email_raises_error(self):
        """
        The test_new_user_with_email_raises_error function tests that the create_user function raises an error if we
        try to pass in a non-string email address.
        We use the assertRaises method of unittest.TestCase to test for this behavior.

        :param self: Access the instance of the class
        :return: An exception
        """
        with self.assertRaises(TypeError) as cm:
            get_user_model().objects.create_user(123, "sample123")

        exception = cm.exception
        self.assertEqual(str(exception), "Email must be an string.")

    def test_create_superuser(self):
        """
        The test_create_superuser function is a test case that checks if the create_superuser function
        in our custom user model works as expected. We first call the create_superuser function with some
        test data and then assert that it returns a user object, which has is_staff and is_superuser set to True.

        :param self: Represent the instance of the class
        :return: A user object
        """
        user = get_user_model().objects.create_superuser("test@example.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_terrain(self):
        """
        The test_create_terrain function is a test case that creating a new terrain successfully

        :param self: Represent the instance of the class
        :return: A terrain object
        """
        terrain = models.Terrain.objects.create(name="desert")

        self.assertIsNotNone(terrain)
        self.assertEqual(terrain.name, "desert")

    def test_create_terrain_repeated(self):
        """
        The test_create_terrain function is a test case that creating a new terrain repeatedly fails

        :param self: Represent the instance of the class
        :return: A terrain object
        """
        models.Terrain.objects.create(name="desert")

        with self.assertRaises(IntegrityError) as cm:
            models.Terrain.objects.create(name="desert")
            self.assertEqual(cm.exception, "Terrain with this name already exists.")

    def test_create_climates(self):
        """
        The test_create_climates function is a test case that creating a new climates successfully

        :param self: Represent the instance of the class
        :return: A climates object
        """
        climate = models.Climate.objects.create(name="climate")

        self.assertIsNotNone(climate)
        self.assertEqual(climate.name, "climate")

    def test_create_climates_repeated(self):
        """
        The test_create_climates function is a test case that creating a new climates repeatedly fails

        :param self: Represent the instance of the class
        :return: A climates object
        """
        models.Climate.objects.create(name="climate")

        with self.assertRaises(IntegrityError) as cm:
            models.Climate.objects.create(name="climate")
            self.assertEqual(cm.exception, "Climate with this name already exists.")

    def test_create_planets(self):
        """
        The test_create_planets function is a test case that creating a new planets successfully

        :param self: Represent the instance of the class
        :return: A planets object
        """
        planet = models.Planet.objects.create(name="planet")

        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "planet")

    def test_create_planets_repeated(self):
        """
        The test_create_planets function is a test case that creating a new planet repeatedly fails

        :param self: Represent the instance of the class
        :return: A planet object
        """
        models.Planet.objects.create(name="planet")

        with self.assertRaises(IntegrityError) as cm:
            models.Planet.objects.create(name="planet")
            self.assertEqual(cm.exception, "Planet with this name already exists.")

    def test_create_planets_with_terrains(self):
        """
        The test_create_planets_with_terrains function is a test case that creating a new planets with terrains
         successfully

        :param self: Represent the instance of the class
        :return: A planets object
        """
        planet = models.Planet.objects.create(name="planet")
        terrain = models.Terrain.objects.create(name="desert")
        planet.terrains.add(terrain)

        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "planet")
        self.assertIn(terrain, planet.terrains.all())

    def test_create_planets_with_climates(self):
        """
        The test_create_planets_with_climates function is a test case that creating a new planets with climates
         successfully.

        :param self: Represent the instance of the class
        :return: A planets object
        """
        planet = models.Planet.objects.create(name="planet")
        climate = models.Climate.objects.create(name="climate")
        planet.climates.add(climate)

        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "planet")
        self.assertIn(climate, planet.climates.all())

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
import json


class TestHomePage(TestCase):
    """Test of the index/hompepage view"""

    def setUp(self):
        self.client = Client()
        self.homepage = reverse("main:index")

    def test_homepage_GET(self):
        """ Testing index / homepage view method """

        response = self.client.get(self.homepage)
        self.assertEquals(response.status_code, 200)
        response = self.client.get("/1")
        self.assertEquals(response.status_code, 404)


class TestRegister(TestCase):
    """Clas to test the register view"""

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user(
            "antoine", "email@email.com", "Password3216854+"
        )

    def test_display_register_view(self):
        response = self.client.get(reverse("main:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password confirmation")

    def can_register_with_post_method(self):
        response = self.client.post(
            "/register/",
            {
                "username": "antoine",
                "password": "Password3216854+",
                "email": "test@test.com",
                "age": "20",
            },
        )
        new_user = MyUser.objects.last()
        self.assertEqual(response.status_code, 304)
        self.assertEquals(new_user.username, "antoine")

    def test_cannot_register_with_incorrect_data(self):
        self.client.post(
            "/register/",
            {
                "username": "antoine",
                "password": "Password3216854+",
                "email": "",
                "age": "20",
            },
        )
        invalid_user = User.objects.filter(email='test@test.com').count()
        self.assertEqual(invalid_user, 0)

    def test_invalid_form(self):
        response = self.client.post(
            "/register/",
            {
                "username": "",
                "password": "Password3216854+",
                "email": "",
                "age": "20",
            },
        )
        self.assertEqual(response.status_code, 200)


class LoginTestView(TestCase):
    '''Class for login viw testing'''

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='antoine',
            password='Password3216854+',
            )

    def test_login_page_display_tested(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)

    def test_get_method_display_method(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_success_login(self):
        response = self.client.post(
            '/login/',
            {'username': 'antoine', 'password': 'Password3216854+'})
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        response = self.client.post(
            '/login/',
            {'username': 'eazezae', 'password': 'ehzae'}
        )
        self.assertEqual(response.status_code, 200)

    def test_already_logged(self):
        self.client.login(username="antoine", password="Password3216854+")
        response = self.client.post('/login/')
        self.assertEqual(response.status_code, 302)


class LogoutTestView(TestCase):
    '''Class used to test logout view function'''

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = User.objects.create_user(
            email='test@test.com',
            username='antoine',
            password='Password1234+')
        self.client.post(
            '/login/',
            {'name': 'test@test.com', 'password': 'Password1234+'})

    def test_logout_successful(self):
        self.client.login(username="antoine", password="Password1234+")
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_redirect(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 302)



from django.test import TestCase, Client
from ..forms import PostForm, SearchForm, ProfilForm, UserFormWithEmail
from ..models import Country
from django.contrib.auth.models import User


class TestPostForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

        self.country = Country.objects.create(
            name="France",
            alpha_2="FR",
            flag="../static/img/flags/flag-FR.jpg",
            resume="La France est un pays d'Europe...",
        )

    def test_valid_post_form(self):
        form_data = {
            "country": "France",
            "city": "Paris",
            "total": 2,
            "wanted": 3,
            "free": 2,
            "interest": "photo",
            "title": "sortie photo",
            "message": "message",
            "start": "2020-10-10",
            "end": "2020-10-10",
            "budget": "20",
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_invalid_post_form(self):
        form_data = {
            "country": "France",
            "city": "Paris",
            "total": "2",
            "wanted": 3,
            "interest": "photo",
            "title": "sortie photo",
            "message": "message",
            "start": "2020-10-10",
            "end": "2020-10-10",
            "budget": "20",
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestSearchForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

    def test_valid_search_form(self):
        form = SearchForm(data={"search": "paris"})
        self.assertTrue(form.is_valid())

    def test_invalid_search_form(self):
        form = SearchForm(data={"searchs": "paris"})
        self.assertFalse(form.is_valid())


class TestProfilForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

    def test_valid_profil_form(self):
        form = ProfilForm(
            data={"username": "test_user", "about": "description"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_profil_form(self):
        form = ProfilForm(
            data={"uusername": "test_user", "about": "description"}
        )
        self.assertFalse(form.is_valid())


class TestUserFormEmail(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

    def test_valid_user_form_email(self):
        form = UserFormWithEmail(
            data={
                "username": "toto",
                "password1": "Password1234+",
                "password2": "Password1234+",
                "email": "test@test.com",
                "age": 20,
            }
        )
        self.assertTrue(form.is_valid())

    def test_save_user(self):
        form = UserFormWithEmail(
            data={
                "username": "toto",
                "password1": "Password1234+",
                "password2": "Password1234+",
                "email": "test@test.com",
                "age": 20,
            }
        )        
        user = form.save()
        self.assertEqual(user, user)


    def test_invalid_user_form_email(self):
        form = UserFormWithEmail(
            data={
                "username": "toto",
                "password1": "Password1234+",
                "password2": "",
                "email": "test@test.com",
                "age": 20,
            }
        )
        self.assertFalse(form.is_valid())

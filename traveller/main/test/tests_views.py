from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from ..views import posts
from ..models import Country, Post, UserAttributes
from datetime import date
import json


class TestAccountPage(TestCase):
    """Test of the index/hompepage view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

    def test_account_redirect(self):
        """ Testing redirect if not logged in """
        response = self.client.get(reverse("main:account"))
        self.assertEquals(response.status_code, 302)

    def test_account_success_display(self):
        """ Testing access page for logged in user """
        user = self.client.login(
            username="test_user", password="Password1234+",
        )
        self.attributs = UserAttributes.objects.create(
            owner=self.user,
            avatar="",
            last_connexion="2020-07-01",
            about="",
            img="base64",
        )

        response = self.client.get(reverse("main:account"))
        self.assertEquals(response.status_code, 200)


class TestPostsPage(TestCase):
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
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )

    def test_invalid_post_GET(self):
        country = self.country.id
        response = self.client.get("main:posts", args=(country,))
        self.assertEqual(response.status_code, 404)


class TestSendPost(TestCase):
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
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )

    def test_send_valid_post(self):
        new_post = self.post.id
        self.client.login(username="test_user", password="Password3216854+")
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )
        post = Post.objects.filter(city="Paris")
        self.assertTrue(post.exists())
        budget = post.values("budget")
        self.assertTrue(budget, "20 euros")


class TestAjaxDeletePost(TestCase):
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
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )

    def test_delete_post_valid_ajax(self):
        self.client.login(username="test_user", password="Password1234+")
        payload = {"post_id": self.post.id}
        response = self.client.post(
            "/delete_post/", payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "deleted"}
        )

    def test_delete_post_invalid_ajax(self):
        self.client.login(username="test_user", password="Password1234+")
        payload = {"post_id": "fake"}
        response = self.client.post(
            "/delete_post/", payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "failed"}
        )


class TestSendMessageAjax(TestCase):
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
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )

    def test_send_valid_message_ajax(self):
        self.client.login(username="test_user", password="Password1234+")
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"message": "SEND OK"}
        )

    def test_send_invalid_message_ajax(self):
        self.client.login(username="test_user", password="Password1d234+")
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"failed": "failed"}
        )

    def test_send_message_ajax_not_logged_in(self):
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)


class TestModifyPostAjax(TestCase):
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
        self.post = Post.objects.create(
            country=self.country,
            creation_date="2019-10-10",
            city="Paris",
            total_travelers="1",
            wanted_travelers="2",
            free_places="1",
            interest="Cuisine",
            title="Cuisine",
            message="Un cours de cuisine à Paris?",
            start_date="2019-10-10",
            end_date="2019-10-10",
            ready=True,
            created_by=self.user,
            budget="20 euros",
        )

    # def test_send_valid_message_ajax(self):
    #     self.client.login(username="test_user", password="Password1234+")
    #     message = {"post_id": self.post.id}
    #     response = self.client.post(
    #         "/modify_post/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    #     )
    #     self.assertEquals(response.status_code, 200)
    #     self.assertJSONEqual(
    #         str(response.content, encoding="utf8"),
    #         {
    #             "post": {
    #                 "budget": "20 euros",
    #                 "city": "Paris",
    #                 "country_id": 1,
    #                 "created_by_id": 1,
    #                 "creation_date": "2020-06-19",
    #                 "end_date": "2019-10-10",
    #                 "free_places": "1",
    #                 "id": 1,
    #                 "interest": "Cuisine",
    #                 "message": "Un cours de cuisine à Paris?",
    #                 "ready": True,
    #                 "start_date": "2019-10-10",
    #                 "title": "Cuisine",
    #                 "total_travelers": "1",
    #                 "wanted_travelers": "2",
    #             },
    #         },
    #     )



class TestSendImageAjax(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )
    
    def test_invalid_send(self):
        self.client.login()
        message = {"img64": "fake image"}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"failed": "failed"}
        )

    # def test_valid_image_send(self):
    #     self.client.login()
    #     message = {"img64": "fake image"}
    #     today = date.today()
    #     user_atts = UserAttributes.objects.create(
    #         owner=self.user,
    #         avatar="",
    #         last_connexion="2019-10-10",
    #         about="",
    #         img=message
    #     )
    #     response = self.client.post(
    #         "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    #     )
    #     self.assertEquals(response.status_code, 200)
    #     self.assertJSONEqual(
    #         str(response.content, encoding="utf8"), {"ok": "ok"}
    #     )
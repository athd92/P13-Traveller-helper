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

    def test_valid_post_GET(self):
        country = self.country.id
        response = self.client.get("/posts/?country_id=1")
        self.assertEqual(response.status_code, 200)

    def test_invalid_int_post_GET(self):
        country = self.country.id
        response = self.client.get("/posts/?country_id=2222222222")
        self.assertEqual(response.status_code, 302)

    def test_invalid_str_post_GET(self):
        country = self.country.id
        response = self.client.get("/posts/?country_id=france")
        self.assertEqual(response.status_code, 302)


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

    def test_visitor_send_invalid_request(self):
        response = self.client.get("/send_post/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_send_post(self):
        self.client.login(username="test_user", password="Password1234+")
        response = self.client.get("/send_post/")
        self.assertEqual(response.status_code, 302)


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

    def test_delete_post_valid_ajax(self) -> dict:
        self.client.login(username="test_user", password="Password1234+")
        payload = {"post_id": self.post.id}
        response = self.client.post(
            "/delete_post/", payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "deleted"}
        )

    def test_delete_post_invalid_ajax(self) -> dict:
        self.client.login(username="test_user", password="Password1234+")
        payload = {"post_id": "fake"}
        response = self.client.post(
            "/delete_post/", payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "failed"}
        )

    def test_visitor_delete_post_invalid_ajax(self) -> dict:
        payload = {"post_id": "fake"}
        response = self.client.post(
            "/delete_post/", payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 302)


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

    def test_send_valid_message_ajax(self) -> dict:
        self.client.login(username="test_user", password="Password1234+")
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"message": "SEND OK"}
        )

    def test_send_invalid_message_ajax(self) -> dict:
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

    def test_send_message_invalid_not_ajax_request(self):
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.get(
            "/send_message/", message, xhr=False)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"failed": "failed"}
        )



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

    def test_send_valid_modification_ajax(self):
        self.client.login(username="test_user", password="Password1234+")
        post_id = {"post_id": self.post.id}
        response = self.client.post(
            "/modify_post/", post_id, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)

    def test_visitor_invalid_request_modification_ajax(self):
        post_id = {"post_id": self.post.id}
        response = self.client.post(
            "/modify_post/", post_id, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 302)


class TestSendImageAjax(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )

    def test_valid_image_send(self) -> dict:

        self.client.login(username="test_user", password="Password1234+")
        message = {"img64": "fake image"}
        today = date.today()
        user_atts = UserAttributes.objects.create(
            owner=self.user,
            avatar="",
            last_connexion=today,
            about="",
            img="img64",
        )
        response = self.client.post(
            "/upload_img/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"ok": "ok"}
        )

    def test_invalid_image_send(self):
        img = {"img64": "fake image"}
        today = date.today()
        user_atts = UserAttributes.objects.create(
            owner=self.user,
            avatar="",
            last_connexion=today,
            about="",
            img="img64",
        )
        response = self.client.post(
            "/upload_img/", img, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 302)

    def test_not_ajax_image_send(self):
        response = self.client.get("/upload_image/")
        self.assertTrue(response.status_code, 302)


        


class TestMessagesPosted(TestCase):
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

    def test_valid_message_request(self) -> dict:
        self.client.login(username="test_user", password="Password1234+")
        response = self.client.get(reverse("main:messages_posted"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "message")

    def test_visitor_message_request(self) -> dict:
        response = self.client.get(reverse("main:messages_posted"))
        self.assertEquals(response.status_code, 302)


class TestDisplayMap(TestCase):
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

    def test_valid_map_display(self):
        city = {"city": "Paris"}
        response = self.client.post(
            "/display_map/", city, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "OK"}
        )

    def test_invalid_map_display(self):
        city = {"czerzeriity": "Paris"}
        response = self.client.post(
            "/display_map/", city, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"result": "failed"}
        )

    def test_not_ajax_map_display(self):
        response = self.client.get("/display_map", {"city": "Paris"})
        self.assertEqual(response.status_code, 301)


class TestUpdateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )
        today = date.today()
        self.user_atts = UserAttributes.objects.create(
            owner=self.user,
            avatar="",
            last_connexion=today,
            about="",
            img="img64",
        )

    def test_valid_update_account(self):
        self.client.login(username="test_user", password="Password1234+")
        response = self.client.post(
            "/update_account/", {"username": "test_user", "about": "à propos"}
        )
        self.assertEqual(response.status_code, 302)

    def test_invalid_update_account(self):
        self.client.login(username="test_user", password="Password1234+")
        response = self.client.post("/update_account/")
        self.assertEqual(response.status_code, 302)

    def test_visitor_update_account(self):
        response = self.client.post("/update_account/")
        self.assertEqual(response.status_code, 302)



class DeleteMessageTest(TestCase):
    """ Testing delete message function"""
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
        self.client.login(username="test_user", password="Password1234+")
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

    def test_delete_message_success(self):
        self.client.login(username="test_user", password="Password1234+")
        message = {"message": "fake valid message", "post_ref": self.post.id}
        response = self.client.post(
            "/send_message/", message, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        response = self.client.post(f"/delete_message/{self.post.id}")
        self.assertEqual(response.status_code, 301)





class TestAjaxGeocode(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_geocode_ajax_request(self):
        datas = {"country": "France", "city": "Paris"}
        response = self.client.post(
            "/get_geocode/", datas, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"coords": {"lat": 48.856614, "lng": 2.3522219}},
        )

    def test_invalid_geocode_ajax_request(self):
        datas = {"country": "ajrazermb", "city": "sdffsdf"}
        response = self.client.post(
            "/get_geocode/", datas, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"coords": {'result': 'no data found'}},
        )


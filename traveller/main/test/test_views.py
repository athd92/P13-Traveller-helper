from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
import json


class TestAccountPage(TestCase):
    """Test of the index/hompepage view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="test_user",
            password="Password1234+",
            email="test@test.com",
        )
        self.client.login(username="test_user", password="Password1234+")
        self.account = reverse("main:account")

    def test_account_redirect(self):
        """ Testing redirect if not logged in """
        response = self.client.get(self.account)
        self.assertEquals(response.status_code, 302)

    def test_account_success_display(self):        
        self.client.login(username="test_user", password="Password1234+")
        response = self.client.get(self.account)
        self.assertEquals(response.status_code, 302)


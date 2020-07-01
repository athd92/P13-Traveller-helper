from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from ..views import index, register, login_request, logout_request, account
from ..views import posts, send_post, delete_post, send_message, modify_post
from ..views import upload_img, display_map, messages_posted


class TestUrl(SimpleTestCase):
    """Calss used to test the uls"""

    def test_index_is_resolved(self):
        url = reverse("main:index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_register_is_resolved(self):
        url = reverse("main:register")
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)

    def test_logout_is_resolved(self):
        url = reverse("main:logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_request)

    def test_login_is_resolved(self):
        url = reverse("main:login")
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_request)

    def test_account_is_resolved(self):
        url = reverse("main:account")
        print(resolve(url))
        self.assertEquals(resolve(url).func, account)

    def test_posts_is_resolved(self):
        url = reverse("main:posts")
        print(resolve(url))
        self.assertEquals(resolve(url).func, posts)

    def test_send_post_is_resolved(self):
        url = reverse("main:send_post")
        print(resolve(url))
        self.assertEquals(resolve(url).func, send_post)

    def test_delete_post_is_resolved(self):
        url = reverse("main:delete_post")
        print(resolve(url))
        self.assertEquals(resolve(url).func, delete_post)

    def test_send_message_is_resolved(self):
        url = reverse("main:send_message")
        print(resolve(url))
        self.assertEquals(resolve(url).func, send_message)

    def test_modify_post_is_resolved(self):
        url = reverse("main:modify_post")
        print(resolve(url))
        self.assertEquals(resolve(url).func, modify_post)

    def test_upload_img_is_resolved(self):
        url = reverse("main:upload_img")
        print(resolve(url))
        self.assertEquals(resolve(url).func, upload_img)

    def test_messages_is_resolved(self):
        url = reverse("main:messages_posted")
        print(resolve(url))
        self.assertEquals(resolve(url).func, messages_posted)

    def test_display_map_is_resolved(self):
        url = reverse("main:display_map")
        print(resolve(url))
        self.assertEquals(resolve(url).func, display_map)

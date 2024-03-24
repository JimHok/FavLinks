from django.test import TestCase
from django.urls import reverse

from .test_authentication import login


class BaseTest(TestCase):
    def setUp(self):
        login(self)
        self.home_url = reverse("links:home")
        self.cat_tag_url = reverse("links:manage_cat_tags")
        return super().setUp()


class favLinksDisplayTest(BaseTest):
    def test_can_display_home_page(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "Favorite Links")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Title")


class catTagDisplayTest(BaseTest):
    def test_can_display_home_page(self):
        response = self.client.get(self.cat_tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Add Category")
        self.assertContains(response, "Add Tag")

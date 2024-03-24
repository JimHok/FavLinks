from django.test import TestCase
from django.urls import reverse

from .test_authentication import login, logout
from .test_add import addLink


class BaseTest(TestCase):
    def setUp(self):
        login(self)
        self.link, self.cat, self.tag, self.tag_2 = addLink()
        self.home_url = reverse("links:home")
        self.cat_tag_url = reverse("links:manage_cat_tags")
        self.update_link_url = reverse("links:update_link", args=[self.link.pk])
        self.update_cat_url = reverse("links:update_cat", args=[self.cat.pk])
        self.update_tag_url = reverse("links:update_tag", args=[self.tag.pk])
        self.cat_new = {"name": "Movie"}
        self.tag_new = {"name": "Java"}
        self.link_new = {"url": "https://www.google.com", "category": 1, "tags": [1, 2]}
        return super().setUp()


class updateCategoryTest(BaseTest):
    def test_can_access_update_category_form(self):
        response = self.client.get(self.update_cat_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Category Form")
        self.assertTemplateUsed(response, "links/link_form.html")
        self.assertContains(response, self.cat.name)

    def test_can_update_category(self):
        response = self.client.post(self.update_cat_url, self.cat_new)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertNotContains(response, self.cat.name)
        self.assertContains(response, self.cat_new["name"])


class updateTagTest(BaseTest):
    def test_can_access_update_tag_form(self):
        response = self.client.get(self.update_tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Tag Form")
        self.assertTemplateUsed(response, "links/link_form.html")
        self.assertContains(response, self.tag.name)

    def test_can_update_tag(self):
        response = self.client.post(self.update_tag_url, self.tag_new)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertNotContains(response, self.tag.name)
        self.assertContains(response, self.tag_new["name"])


class updateLinkTest(BaseTest):

    def test_can_access_update_link_form(self):
        response = self.client.get(self.update_link_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "links/link_form.html")
        self.assertContains(response, self.link.title)

    def test_can_update_link(self):
        response = self.client.post(self.update_link_url, self.link_new)
        self.client.post(self.update_cat_url, self.cat_new)
        self.client.post(self.update_tag_url, self.tag_new)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        response = self.client.get(self.home_url)
        self.assertNotContains(response, self.link.url)
        self.assertContains(response, self.link_new["url"])
        self.assertContains(response, self.cat_new["name"])
        self.assertContains(response, self.tag_new["name"])

    def test_update_link_unauthorized(self):
        logout(self)
        response = self.client.get(self.update_link_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/update_link/1/")

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
        self.delete_link_url = reverse("links:delete_link", args=[self.link.pk])
        self.delete_cat_url = reverse("links:delete_cat", args=[self.cat.pk])
        self.delete_tag_url = reverse("links:delete_tag", args=[self.tag.pk])
        return super().setUp()


class deleteCategoryTest(BaseTest):
    def test_can_access_delete_category_form(self):
        response = self.client.get(self.delete_cat_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Delete Confirmation")
        self.assertTemplateUsed(response, "links/delete.html")
        self.assertContains(response, self.cat.name)

    def test_can_delete_category(self):
        response = self.client.post(self.delete_cat_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertNotContains(response, self.cat.name)


class deleteTagTest(BaseTest):
    def test_can_access_delete_tag_form(self):
        response = self.client.get(self.delete_tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Delete Confirmation")
        self.assertTemplateUsed(response, "links/delete.html")
        self.assertContains(response, self.tag.name)

    def test_can_delete_tag(self):
        response = self.client.post(self.delete_tag_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertNotContains(response, self.tag.name)
        self.assertContains(response, self.tag_2.name)


class deleteLinkTest(BaseTest):

    def test_can_access_delete_link_form(self):
        response = self.client.get(self.delete_link_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "links/delete.html")
        self.assertContains(response, self.link.title)

    def test_can_delete_link(self):
        response = self.client.post(self.delete_link_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        response = self.client.get(self.home_url)
        self.assertNotContains(response, self.link.url)

    def test_delete_link_unauthorized(self):
        logout(self)
        response = self.client.get(self.delete_link_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/delete_link/1/")

from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("links:register")


class RegisterTest(BaseTest):
    def test_register_page_status_code(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")

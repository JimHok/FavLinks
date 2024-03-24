from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("links:register")
        self.login_url = reverse("links:login")
        self.logout_url = reverse("links:logout")
        self.user = {
            "username": "testuser",
            "password1": "111111Tt",
            "password2": "111111Tt",
        }
        self.user_short_password = {
            "username": "testuser",
            "password1": "111",
            "password2": "111",
        }
        self.user_not_matching_password = {
            "username": "testuser",
            "password1": "111111Tt",
            "password2": "111111T",
        }
        self.user_only_number_password = {
            "username": "testuser",
            "password1": "111111",
            "password2": "111111",
        }
        self.user_register = {
            "username": "testuser",
            "password1": "111111Tt",
            "password2": "111111Tt",
        }
        self.user_login = {
            "username": "testuser",
            "password": "111111Tt",
        }
        self.user_login_wrong = {
            "username": "testuser",
            "password": "111111T",
        }
        return super().setUp()


def login(self):
    self.register_url = reverse("links:register")
    self.login_url = reverse("links:login")
    self.user_register = {
        "username": "testuser",
        "password1": "111111Tt",
        "password2": "111111Tt",
    }
    self.user_login = {
        "username": "testuser",
        "password": "111111Tt",
    }
    self.client.post(self.register_url, self.user_register)
    self.client.post(self.login_url, self.user_login)


class RegisterTest(BaseTest):
    def test_register_page_status_code(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")

    def test_can_register(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("links:login"))

    def test_cant_register_with_short_password(self):
        response = self.client.post(self.register_url, self.user_short_password)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")
        self.assertTemplateNotUsed(response, "links/login.html")
        self.assertContains(
            response,
            "This password is too short. It must contain at least 8 characters.",
        )

    def test_cant_register_with_not_matching_password(self):
        response = self.client.post(self.register_url, self.user_not_matching_password)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")
        self.assertTemplateNotUsed(response, "links/login.html")
        self.assertContains(response, "The two password fields didn’t match.")

    def test_cant_register_with_only_number_password(self):
        response = self.client.post(self.register_url, self.user_only_number_password)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")
        self.assertTemplateNotUsed(response, "links/login.html")
        self.assertContains(response, "This password is entirely numeric.")

    def test_cant_register_with_existing_username(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/register.html")
        self.assertTemplateNotUsed(response, "links/login.html")


class LoginTest(BaseTest):

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/login.html")

    def test_can_login(self):
        self.client.post(self.register_url, self.user_register)
        response = self.client.post(self.login_url, self.user_login)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("links:home"))

    def test_cant_login_with_wrong_password(self):
        self.client.post(self.register_url, self.user_register)
        response = self.client.post(self.login_url, self.user_login_wrong)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "links/login.html")
        self.assertTemplateNotUsed(response, "links/home.html")
        self.assertContains(response, "Username or password is incorrect")


def logout(self):
    self.logout_url = reverse("links:logout")
    self.client.get(self.logout_url)


class LogoutTest(BaseTest):

    def test_can_logout(self):
        login(self)
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

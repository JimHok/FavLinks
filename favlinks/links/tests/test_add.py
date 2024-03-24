from django.test import TestCase
from django.urls import reverse
import requests
from bs4 import BeautifulSoup

from .test_authentication import login
from links.models import FavLink, Category, Tag


class BaseTest(TestCase):
    def setUp(self):
        login(self)
        self.home_url = reverse("links:home")
        self.cat_tag_url = reverse("links:manage_cat_tags")
        self.add_link_url = reverse("links:add_link")
        self.add_cat_url = reverse("links:add_cat")
        self.add_tag_url = reverse("links:add_tag")
        self.category = {"name": "Video"}
        self.tags = {"name": "Python"}
        self.tags_2 = {"name": "Django"}
        self.link_title = {"title": "Hello"}
        self.link_category = {"category": 1}
        self.link_tags = {"tags": [1, 2]}
        self.add_link_with_url = {
            "url": "https://www.youtube.com",
        }
        self.add_link_with_url_title = dict(self.add_link_with_url, **self.link_title)
        self.add_link_with_url_cat = dict(self.add_link_with_url, **self.link_category)
        self.add_link_with_url_tag = dict(self.add_link_with_url, **self.link_tags)
        self.add_link_with_url_cat_tag = dict(
            self.add_link_with_url, **self.link_category, **self.link_tags
        )
        self.add_link_with_wrong_url = {"url": "https://www.youtube,com"}
        return super().setUp()


class addCategoryTest(BaseTest):
    def test_can_access_add_category_form(self):
        response = self.client.get(self.add_cat_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Category Form")

    def test_can_add_category(self):
        response = self.client.post(self.add_cat_url, self.category)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertContains(response, self.category["name"])


class addTagTest(BaseTest):
    def test_can_access_add_tag_form(self):
        response = self.client.get(self.add_tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Tag Form")

    def test_can_add_tag(self):
        response = self.client.post(self.add_tag_url, self.tags)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.cat_tag_url)
        response = self.client.get(self.cat_tag_url)
        self.assertContains(response, self.tags["name"])


def addCatTag(self):
    self.add_cat_url = reverse("links:add_cat")
    self.add_tag_url = reverse("links:add_tag")
    self.category = {"name": "Video"}
    self.tags = {"name": "Python"}
    self.tags_2 = {"name": "Django"}
    self.client.post(self.add_cat_url, self.category)
    self.client.post(self.add_tag_url, self.tags)
    self.client.post(self.add_tag_url, self.tags_2)


def addLink(
    user_id=1,
    link="https://www.youtube.com",
    cat_name="Video",
    tag_name_1="Python",
    tag_name_2="Django",
):
    user_id = user_id
    cat = Category.objects.create(name=cat_name, user_id=user_id)
    tag = Tag.objects.create(name=tag_name_1, user_id=user_id)
    tag_2 = Tag.objects.create(name=tag_name_2, user_id=user_id)
    link = FavLink.objects.create(
        url=link,
        category=cat,
        user_id=user_id,
    )
    link.tags.add(tag, tag_2)

    return link, cat, tag, tag_2


def getTitle(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string[:50]
    return title


class addLinkTest(BaseTest):
    def test_can_access_add_link_form(self):
        response = self.client.get(self.add_link_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Link Form")

    def test_can_add_link_with_url(self):
        response = self.client.post(self.add_link_url, self.add_link_with_url)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(self.home_url)
        self.assertContains(response, self.add_link_with_url["url"])
        title = getTitle(self.add_link_with_url["url"])
        self.assertContains(response, title)
        self.assertContains(response, "None")

    def test_can_add_link_with_url_title(self):
        response = self.client.post(self.add_link_url, self.add_link_with_url_title)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(self.home_url)
        self.assertContains(response, self.add_link_with_url["url"])
        title = self.link_title["title"]
        self.assertContains(response, title)
        self.assertContains(response, "None")

    def test_can_add_link_with_url_cat(self):
        addCatTag(self)
        response = self.client.post(self.add_link_url, self.add_link_with_url_cat)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(self.home_url)
        self.assertContains(response, self.add_link_with_url["url"])
        title = getTitle(self.add_link_with_url["url"])
        self.assertContains(response, title)
        self.assertContains(response, self.category["name"])

    def test_can_add_link_with_url_tag(self):
        addCatTag(self)
        response = self.client.post(self.add_link_url, self.add_link_with_url_tag)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(self.home_url)
        self.assertContains(response, self.add_link_with_url["url"])
        title = getTitle(self.add_link_with_url["url"])
        self.assertContains(response, title)
        self.assertContains(response, self.tags["name"])
        self.assertContains(response, self.tags_2["name"])

    def test_can_add_link_with_url_cat_tag(self):
        addCatTag(self)
        response = self.client.post(self.add_link_url, self.add_link_with_url_cat_tag)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(self.home_url)
        self.assertContains(response, self.add_link_with_url["url"])
        title = getTitle(self.add_link_with_url["url"])
        self.assertContains(response, title)
        self.assertContains(response, self.category["name"])
        self.assertContains(response, self.tags["name"])
        self.assertContains(response, self.tags_2["name"])

    def test_cant_add_link_with_wrong_url(self):
        response = self.client.post(self.add_link_url, self.add_link_with_wrong_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Error: URL not valid.")

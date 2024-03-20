from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")


class Tag(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")


class FavLink(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=50)
    url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="links", null=True
    )
    tags = models.ManyToManyField(Tag, related_name="links", blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")

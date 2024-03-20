from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django import forms

from django.forms import ModelForm, HiddenInput
from .models import *


class FavoriteLinkForm(ModelForm):
    class Meta:
        model = FavLink
        fields = ["url", "title", "category", "tags", "status"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"] = forms.CharField(widget=HiddenInput())
        self.fields["title"].required = False
        self.fields["title"].widget.attrs["placeholder"] = "Title will be auto fetched"
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)
            self.fields["tags"].queryset = Tag.objects.filter(user=user)
        else:
            self.fields["category"].queryset = Category.objects.none()
            self.fields["tags"].queryset = Tag.objects.none()
        self.fields["category"].required = False
        self.fields["tags"].required = False


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

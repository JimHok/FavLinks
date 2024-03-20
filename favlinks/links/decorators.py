from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("links:home"))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

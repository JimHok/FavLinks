from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.core.cache import cache

import requests
import threading
from bs4 import BeautifulSoup
import json
from rich.console import Console
from rich.traceback import install

install()

from .models import *
from .forms import CreateUserForm, FavoriteLinkForm, CategoryForm, TagForm
from .filters import FavLinkFilter
from .decorators import unauthenticated_user
from .tasks import get_links


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.cleaned_data.get("username")
            # messages.success(request, "Account was created for " + user)
            return redirect(reverse("links:login"))
    context = {"form": form}
    return render(request, "links/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("links:home"))
        else:
            messages.info(request, "Username or password is incorrect")
    context = {}
    return render(request, "links/login.html", context)


@login_required(login_url="links:login")
def logoutUser(request):
    logout(request)
    return redirect(reverse("links:login"))


@login_required(login_url="links:login")
def home(request):

    fav_links = FavLink.objects.filter(user=request.user).order_by("-date")

    myFilter = FavLinkFilter(request.user, request.GET, queryset=fav_links)
    fav_links = myFilter.qs

    paginator = Paginator(fav_links, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"myFilter": myFilter, "page_obj": page_obj}
    return render(request, "links/fav_links.html", context)


@login_required(login_url="links:login")
def manageCatTags(request):
    categories = Category.objects.filter(user=request.user).annotate(
        num_links=Count("links")
    )
    tags = Tag.objects.filter(user=request.user).annotate(num_links=Count("links"))
    context = {"categories": categories, "tags": tags}
    return render(request, "links/manage_cat_tags.html", context)


@login_required(login_url="links:login")
def handle_generic_link_form(request, pk=None, category=None):
    instance = None
    if pk:
        instance = FavLink.objects.get(id=pk)
        # If the user is adding a new link, check if the background task
        # for checking link validity is still running. If it is, redirect
        # the user to the home page and display an error message.
        if not cache.get("links_updated"):
            messages.error(
                request, "URLs validity checking in progress, please wait a moment..."
            )
            return redirect("/")

    # Instantiate the form.
    form = FavoriteLinkForm(request.user, instance=instance)

    # If the form is being submitted, check the URL and update the form
    # with the title and status of the URL if it is valid.
    if request.method == "POST":
        try:
            # Get the response from the URL and parse it with BeautifulSoup.
            response = requests.get(request.POST.get("url"))
            soup = BeautifulSoup(response.text, "html.parser")

            # Get the title of the page.
            title = soup.title.string[:50]

            # Make a mutable copy of the POST data so we can modify it.
            mutable_post = request.POST.copy()
            print(mutable_post)

            # If the title is blank or None, auto fill the title of the page from the URL request.
            if request.POST.get("title") == "" or request.POST.get("title") is None:
                mutable_post["title"] = title

            # Set the status of the link based on the HTTP status code.
            mutable_post["status"] = response.status_code == 200

            # If a category was specified, add it to the form data.
            if category:
                mutable_post["category"] = category

            # Instantiate a new FavoriteLinkForm with the modified POST data.
            form = FavoriteLinkForm(request.user, mutable_post, instance=instance)

            # If the form is valid, save the link and display a success message.
            if form.is_valid():
                favorite_link = form.save(commit=False)
                favorite_link.user = request.user
                form.save()
                messages.success(
                    request, f"Link {'updated' if pk else 'added'} successfully!"
                )
                return redirect("/")

        # If there was an error with the URL, display an error message.
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error: URL not valid.")

        except Exception as e:
            messages.error(request, f"Error: {e}")

    # If the form is not being submitted or there was an error, render the form.
    context = {"form": form, "title": "Link Form"}
    return render(request, "links/link_form.html", context)


@login_required(login_url="links:login")
def addLink(request, category=None):
    return handle_generic_link_form(request, category=category)


@login_required(login_url="links:login")
def updateLink(request, pk, category=None):
    return handle_generic_link_form(request, pk=pk, category=category)


@login_required(login_url="links:login")
def deleteLink(request, pk):
    if not cache.get("links_updated"):
        messages.error(
            request, "URLs validity checking in progress, please wait a moment..."
        )
        return redirect("/")
    fav_link = FavLink.objects.get(id=pk)
    if request.method == "POST":
        fav_link.delete()
        return redirect("/")
    context = {"item": fav_link.title}
    return render(request, "links/delete.html", context)


@login_required(login_url="links:login")
def handle_generic_form(request, FormClass, template_name, success_url_name, pk=None):
    instance = None
    if pk:
        instance = FormClass.Meta.model.objects.get(id=pk)
    form = FormClass(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            form.save()
            return redirect(reverse("links:" + success_url_name))
    return render(
        request,
        template_name,
        {"form": form, "title": FormClass._meta.model.__name__ + " Form"},
    )


@login_required(login_url="links:login")
def handle_generic_delete(request, ModelClass, success_url_name, pk):
    item = ModelClass.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect(reverse("links:" + success_url_name))
    return render(request, "links/delete.html", {"item": item.name})


@login_required(login_url="links:login")
def addCategory(request):
    return handle_generic_form(
        request, CategoryForm, "links/link_form.html", "manage_cat_tags"
    )


@login_required(login_url="links:login")
def updateCategory(request, pk):
    return handle_generic_form(
        request, CategoryForm, "links/link_form.html", "manage_cat_tags", pk
    )


@login_required(login_url="links:login")
def deleteCategory(request, pk):
    return handle_generic_delete(request, Category, "manage_cat_tags", pk)


@login_required(login_url="links:login")
def addTag(request):
    return handle_generic_form(
        request, TagForm, "links/link_form.html", "manage_cat_tags"
    )


@login_required(login_url="links:login")
def updateTag(request, pk):
    return handle_generic_form(
        request, TagForm, "links/link_form.html", "manage_cat_tags", pk
    )


@login_required(login_url="links:login")
def deleteTag(request, pk):
    return handle_generic_delete(request, Tag, "manage_cat_tags", pk)


@login_required(login_url="links:login")
def urlCheck(request):
    get_links.delay()
    return redirect("/")


# @login_required(login_url="links:login")
def scheduleTask(request):

    interval, _ = IntervalSchedule.objects.get_or_create(
        every=10, period=IntervalSchedule.SECONDS
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="get-link",
        task="links.tasks.get_links",
    )

    return HttpResponse("Task scheduled!")


@login_required(login_url="links:login")
def commandLineInterface(request):
    form = FavoriteLinkForm(request.user)
    fav_links = FavLink.objects.filter(user=request.user).order_by("-date")
    categories = Category.objects.filter(user=request.user).annotate(
        num_links=Count("links")
    )
    if request.method == "POST":
        try:
            category = None
            if request.POST.get("method") == "add":
                if request.POST.get("category"):
                    category = [
                        cat.pk
                        for cat in categories
                        if cat.name == request.POST.get("category")
                    ][0]
                return addLink(request, category)
            if request.POST.get("method") == "update":
                if request.POST.get("category"):
                    category = [
                        cat.pk
                        for cat in categories
                        if cat.name == request.POST.get("category")
                    ][0]
                return updateLink(request, request.POST.get("id"), category)
            if request.POST.get("method") == "delete":
                return deleteLink(request, request.POST.get("id"))
        except Exception as e:
            print(e)
            context = {"error": True}
            return HttpResponse("error")
    context = {"fav_links": fav_links, "categories": categories}
    return render(request, "links/cli.html", context)

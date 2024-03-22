from celery import shared_task
from .models import *
import requests
from django.core.cache import cache


@shared_task()
def get_links():
    cache.set("links_updated", False, timeout=None)
    fav_links = FavLink.objects.all()
    links = [link for link in fav_links]

    for link in links:
        response = requests.get(link.url)
        link.status = response.status_code == 200
        print(f"URL: {str(link.url)}\n Status: {str(link.status)}")
        link.save()

    cache.set("links_updated", True, timeout=None)
    return "Task completed!"

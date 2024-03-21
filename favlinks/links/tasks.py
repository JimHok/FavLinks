from celery import shared_task
from .models import *
import requests


@shared_task()
def get_links():

    fav_links = FavLink.objects.all()
    links = [link for link in fav_links]

    for link in links:
        response = requests.get(link.url)
        print(link.url)
        link.status = response.status_code == 200
        print(link.status)
        link.save()

    return "Task completed!"

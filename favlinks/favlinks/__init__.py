from .celery import app as celery_app
from django.core.cache import cache

__all__ = ("celery_app",)

cache.set("links_updated", True, timeout=None)

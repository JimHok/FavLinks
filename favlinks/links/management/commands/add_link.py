from django.core.cache import cache
import djclick as click
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.forms import FavoriteLinkForm
from links.models import Category, Tag

console = Console()
install()


@click.command()
@click.option("--url", prompt="URL", help="URL text that should be valid")
@click.option(
    "--category",
    prompt="Category {cat}".format(
        cat=[
            {str(category.pk): category.name}
            for category in Category.objects.filter(user=cache.get("cli_user"))
        ]
    ),
    help="Category should be the id number of the category",
)
@click.option(
    "--tags",
    prompt="Tags {tag}".format(
        tag=[
            {str(tag.pk): tag.name}
            for tag in Tag.objects.filter(user=cache.get("cli_user"))
        ]
    ),
    help="Tags should be id number of tags and separated by spaces",
)
def add_links_command(url, category, tags):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string[:50]
        status = response.status_code == 200
    except requests.exceptions.RequestException as e:
        console.print(Panel(f"Error: {e}", style="red"))
        return
    except Exception as e:
        console.print(Panel(f"An unexpected error occurred: {e}", style="red"))
        return

    category = category if category != "None" else None
    tags = list(tags.split(" ")) if tags != "None" else []

    post_data = {
        "url": url,
        "title": title,
        "category": category,
        "tags": tags,
        "status": status,
    }

    form = FavoriteLinkForm(user, post_data)

    if form.is_valid():
        favorite_link = form.save(commit=False)
        favorite_link.user = user
        form.save()

        console.print(Panel.fit(f"Link added successfully!", style="green"))

    else:
        for error in form.errors.values():
            cleaned_error = strip_tags(str(error))
            console.print(Panel.fit(f"Error: {cleaned_error}", style="red"))

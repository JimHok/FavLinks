from django.core.cache import cache
import djclick as click
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.models import Category

console = Console()
install()


@click.command()
@click.option(
    "--id",
    prompt="Category {cat}".format(
        cat=[
            {str(cat.pk): cat.name}
            for cat in Category.objects.filter(user=cache.get("cli_user"))
        ]
    ),
    help="Id should be the id number of the category",
)
def delete_cat_command(id):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    cat = Category.objects.get(id=id)
    cat.delete()

    console.print(Panel.fit(f"Link deleted successfully!", style="green"))

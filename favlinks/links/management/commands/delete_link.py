from django.core.cache import cache
import djclick as click
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.models import FavLink

console = Console()
install()


@click.command()
@click.option(
    "--id",
    prompt="FavLinks {favlinks}".format(
        favlinks=[
            {str(favlink.pk): favlink.title}
            for favlink in FavLink.objects.filter(user=cache.get("cli_user"))
        ]
    ),
    help="Id should be the id number of the link",
)
def delete_link_command(id):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    fav_link = FavLink.objects.get(id=id)
    fav_link.delete()

    console.print(Panel.fit(f"Link deleted successfully!", style="green"))

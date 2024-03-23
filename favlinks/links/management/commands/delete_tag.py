from django.core.cache import cache
import djclick as click
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.models import Tag

console = Console()
install()


@click.command()
@click.option(
    "--id",
    prompt="Tag {tag}".format(
        tag=[
            {str(tag.pk): tag.name}
            for tag in Tag.objects.filter(user=cache.get("cli_user"))
        ]
    ),
    help="Id should be the id number of the tag",
)
def delete_tag_command(id):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    tag = Tag.objects.get(id=id)
    tag.delete()

    console.print(Panel.fit(f"Link deleted successfully!", style="green"))

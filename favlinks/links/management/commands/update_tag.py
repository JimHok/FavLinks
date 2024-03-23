from django.core.cache import cache
import djclick as click
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.forms import TagForm
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
    help="Id should be the id number of the link",
)
@click.option(
    "--tag",
    prompt="Tag",
    help="Input is the name of new tag",
)
def update_tag_command(id, tag):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")

    post_data = {
        "name": tag,
    }

    form = TagForm(post_data, instance=Tag.objects.get(id=id))

    if form.is_valid():
        tag_list = form.save(commit=False)
        tag_list.user = user
        form.save()

        console.print(Panel.fit(f"Link updated successfully!", style="green"))

    else:
        for error in form.errors.values():
            console.print(Panel.fit(f"[red]Error: {error}[/red]"))

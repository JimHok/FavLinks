from django.core.cache import cache
import djclick as click
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.forms import CategoryForm
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
    help="Id should be the id number of the link",
)
@click.option(
    "--category",
    prompt="Category",
    help="Input is the name of new category",
)
def update_cat_command(id, category):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")

    post_data = {
        "name": category,
    }

    form = CategoryForm(post_data, instance=Category.objects.get(id=id))

    if form.is_valid():
        category_list = form.save(commit=False)
        category_list.user = user
        form.save()

        console.print(Panel.fit(f"Link updated successfully!", style="green"))

    else:
        for error in form.errors.values():
            console.print(Panel.fit(f"[red]Error: {error}[/red]"))

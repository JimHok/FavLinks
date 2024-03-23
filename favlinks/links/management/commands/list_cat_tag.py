from django.core.cache import cache
import djclick as click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.models import Category, Tag

console = Console()
install()


@click.command()
def disp_cat_tag_command():
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")
    categories = Category.objects.filter(user=user)

    tags = Tag.objects.filter(user=user)
    panel = Panel.fit(
        f"{[{cat.pk: cat.name} for cat in categories]}",
        title="Category Details",
        border_style="green",
    )
    console.print(panel)
    panel = Panel.fit(
        f"{[{tag.pk: tag.name} for tag in tags]}",
        title="Tag Details",
        border_style="green",
    )
    console.print(panel)

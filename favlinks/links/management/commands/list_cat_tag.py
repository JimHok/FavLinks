from django.core.cache import cache
import djclick as click
from django.db.models import Count
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install
from rich.table import Table
from rich.columns import Columns

from links.models import Category, Tag

console = Console()
install()


@click.command()
def disp_cat_tag_command():
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")
    categories = Category.objects.filter(user=user).annotate(num_links=Count("links"))

    tags = Tag.objects.filter(user=user).annotate(num_links=Count("links"))

    table_cat = Table(title="Categories Detail", show_lines=True, style="green")
    table_cat.add_column("ID")
    table_cat.add_column("Name")
    table_cat.add_column("Associated URL")
    for cat in categories:
        table_cat.add_row(
            str(cat.pk),
            cat.name,
            str(cat.num_links),
        )

    table_tag = Table(title="Tags Detail", show_lines=True, style="green")
    table_tag.add_column("ID")
    table_tag.add_column("Name")
    table_tag.add_column("Associated URL")
    for tag in tags:
        table_tag.add_row(
            str(tag.pk),
            tag.name,
            str(tag.num_links),
        )

    column = Columns(
        [table_cat, table_tag],
    )

    console.print(column)

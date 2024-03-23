from django.core.cache import cache
import djclick as click
from django.db.models import Q
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install

from links.models import FavLink, Category, Tag

console = Console()
install()


@click.command()
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
def filter_command(category, tags):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")
    category = category if category != "None" else Q()
    tags = list(tags.split(" ")) if tags != "None" else Q()
    fav_links = FavLink.objects.filter(
        user=user, category=category, tags__in=tags
    ).order_by("-date")
    table_link = Table(
        title="Favorite Links Detail",
        show_lines=True,
        style="green",
    )
    table_link.add_column("ID")
    table_link.add_column("Title")
    table_link.add_column("URL")
    table_link.add_column("Category")
    table_link.add_column("Tags")
    table_link.add_column("Status")
    table_link.add_column("Date")

    for link in fav_links:
        tags = [tag.name for tag in link.tags.all()]
        tags_str = ", ".join(tags) if tags else "No tags"
        status = "Online" if link.status else "Offline"
        category_str = link.category.name if link.category else "No category"
        table_link.add_row(
            str(link.pk),
            link.title,
            link.url,
            category_str,
            tags_str,
            status,
            str(link.date),
        )

    console.print(table_link)

from django.core.cache import cache
import djclick as click
from django.db.models import Q
from rich.console import Console
from rich.panel import Panel
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
    ).order_by("date")
    for link in fav_links:
        tags = [
            tag.name for tag in link.tags.all()
        ]  # Get the names of the related tags
        tags_str = ", ".join(tags) if tags else "No tags"
        panel = Panel.fit(
            f"[bold]ID:[/bold] {link.pk}\n"
            f"[bold]Title:[/bold] {link.title}\n"
            f"[bold]URL:[/bold] {link.url}\n"
            f"[bold]Category:[/bold] {link.category}\n"
            f"[bold]Tags:[/bold] {tags_str}\n"
            f"[bold]Status:[/bold] {link.status}\n"
            f"[bold]Date:[/bold] {link.date}",
            title="Link Details",
            border_style="green",
        )
        console.print(panel)

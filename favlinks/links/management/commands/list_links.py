from django.core.cache import cache
import djclick as click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.models import FavLink

console = Console()
install()


@click.command()
def disp_links_command():
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")
    fav_links = FavLink.objects.filter(user=user).order_by("date")
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

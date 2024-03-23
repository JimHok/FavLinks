from django.contrib.auth import authenticate
from django.core.cache import cache
import djclick as click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

console = Console()
install()


@click.command()
def login_command():
    user = cache.get("cli_user")
    if user is not None:
        cache.set("cli_user", None, timeout=None)
        console.print(Panel.fit(f"Logout successful user: {user}", style="green"))

    else:
        console.print(Panel.fit("User not logged in yet!", style="red"))

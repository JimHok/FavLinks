from django.contrib.auth import authenticate
from django.core.cache import cache
import djclick as click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

console = Console()
install()


@click.command()
@click.option("--username", prompt="Username", help="Username")
@click.option("--password", prompt="Password", help="Password", hide_input=True)
def login_command(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        cache.set("cli_user", user, timeout=None)
        console.print(Panel.fit(f"Login successful user: {user}", style="green"))

    else:
        console.print(Panel.fit("Invalid credentials", style="red"))

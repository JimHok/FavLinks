from django.contrib.auth import authenticate
from django.utils.html import strip_tags
from django.core.cache import cache
import djclick as click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.forms import CreateUserForm

console = Console()
install()


@click.command()
@click.option("--username", prompt="Username", help="Username")
@click.option("--password1", prompt="Password", help="Password", hide_input=True)
@click.option(
    "--password2", prompt="Confirm Password", help="Re-enter Password", hide_input=True
)
def login_command(username, password1, password2):
    user = authenticate(username=username, password=password1)
    if user != cache.get("cli_user") and cache.get("cli_user") is not None:
        console.print(Panel.fit("User already logged in", style="red"))
        return

    if password1 != password2:
        console.print(Panel.fit("Passwords do not match", style="red"))
        return

    post_data = {
        "username": username,
        "password1": password1,
        "password2": password2,
    }

    form = CreateUserForm(post_data)
    if form.is_valid():
        form.save()
    else:
        for error in form.errors.values():
            cleaned_error = strip_tags(str(error))
            console.print(Panel.fit(f"Error: {cleaned_error}", style="red"))

    user = authenticate(username=username, password=password1)
    if user is not None:
        console.print(Panel.fit(f"Registration successful user: {user}", style="green"))

    else:
        console.print(Panel.fit("Registration failed", style="red"))

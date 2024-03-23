from django.core.cache import cache
import djclick as click
from django.utils.html import strip_tags
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from links.forms import CategoryForm

console = Console()
install()


@click.command()
@click.option(
    "--category",
    prompt="Category",
    help="Input is the name of new category",
)
def add_cat_command(category):
    if cache.get("cli_user") is None:
        console.print(Panel.fit("User not logged in yet!", style="red"))
        return
    user = cache.get("cli_user")

    post_data = {
        "name": category,
    }

    form = CategoryForm(post_data)

    if form.is_valid():
        category_list = form.save(commit=False)
        category_list.user = user
        form.save()

        console.print(Panel.fit(f"Category added successfully!", style="green"))

    else:
        for error in form.errors.values():
            cleaned_error = strip_tags(str(error))
            console.print(Panel.fit(f"Error: {cleaned_error}", style="red"))

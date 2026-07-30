from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_technology(target: Target) -> None:
    table = Table(title="Technology Information")

    table.add_column("Technology", style="cyan")

    technologies = target.results.technology.technologies

    if not technologies:
        table.add_row("-")
    else:
        for technology in technologies:
            table.add_row(technology)

    console.print(table)
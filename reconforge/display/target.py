from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_target(target: Target) -> None:
    table = Table(title="Target Information")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Type", target.target_type)
    table.add_row("Hostname", str(target.hostname))
    table.add_row("IP", str(target.ip))
    table.add_row("Scheme", str(target.scheme))
    table.add_row("Port", str(target.port))

    console.print(table)
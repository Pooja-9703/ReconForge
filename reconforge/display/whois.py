from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_whois(target: Target) -> None:
    table = Table(title="WHOIS Information")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    whois = target.results.whois

    table.add_row("Registrar", whois.registrar or "-")
    table.add_row("Creation Date", whois.creation_date or "-")
    table.add_row("Expiration Date", whois.expiration_date or "-")
    table.add_row("Updated Date", whois.updated_date or "-")

    table.add_row(
        "Name Servers",
        ", ".join(whois.name_servers)
        if whois.name_servers
        else "-",
    )

    console.print(table)
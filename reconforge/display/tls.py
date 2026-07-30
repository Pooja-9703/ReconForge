from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_tls(target: Target) -> None:
    table = Table(title="TLS Information")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    tls = target.results.tls

    table.add_row("Subject", tls.subject or "-")
    table.add_row("Issuer", tls.issuer or "-")
    table.add_row(
        "SANs",
        ", ".join(tls.sans) if tls.sans else "-",
    )
    table.add_row("Valid From", tls.valid_from or "-")
    table.add_row("Valid Until", tls.valid_until or "-")

    if tls.days_remaining is None:
        days = "-"
    elif tls.days_remaining < 30:
        days = f"[red]{tls.days_remaining}[/red]"
    elif tls.days_remaining < 90:
        days = f"[yellow]{tls.days_remaining}[/yellow]"
    else:
        days = f"[green]{tls.days_remaining}[/green]"

    table.add_row("Days Remaining", days)

    table.add_row("TLS Version", tls.tls_version or "-")
    table.add_row("Cipher", tls.cipher or "-")

    console.print(table)
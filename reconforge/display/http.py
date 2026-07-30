from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_http(target: Target) -> None:
    table = Table(title="HTTP Information")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    http = target.results.http

    table.add_row("Status Code", str(http.status_code or "-"))
    table.add_row("Server", http.server or "-")
    table.add_row("Content-Type", http.content_type or "-")
    table.add_row(
        "Content-Length",
        str(http.content_length)
        if http.content_length is not None
        else "-",
    )
    table.add_row("Redirect URL", http.redirect_url or "-")
    table.add_row("Title", http.title or "-")
    table.add_row(
        "Response Time",
        f"{http.response_time} ms"
        if http.response_time is not None
        else "-",
    )

    console.print(table)
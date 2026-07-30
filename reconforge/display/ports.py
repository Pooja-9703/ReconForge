from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_ports(target: Target) -> None:
    table = Table(title="Port Scan")

    table.add_column("Port", style="cyan")
    table.add_column("Service", style="green")
    table.add_column("Banner", style="yellow")

    ports = target.results.ports.open_ports

    if not ports:
        table.add_row("-", "-", "-")
    else:
        for port in ports:
            table.add_row(
                str(port.port),
                port.service,
                port.banner,
            )

    console.print(table)
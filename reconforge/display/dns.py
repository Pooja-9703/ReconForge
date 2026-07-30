from rich.console import Console
from rich.table import Table

from reconforge.models.target import Target

console = Console()


def display_dns(target: Target) -> None:
    table = Table(title="DNS Information")

    table.add_column("Record", style="cyan")
    table.add_column("Value", style="green")

    dns = target.results.dns

    table.add_row(
        "A",
        ", ".join(dns.a_records) if dns.a_records else "-"
    )

    table.add_row(
        "AAAA",
        ", ".join(dns.aaaa_records) if dns.aaaa_records else "-"
    )

    table.add_row(
        "MX",
        ", ".join(dns.mx_records) if dns.mx_records else "-"
    )

    table.add_row(
        "NS",
        ", ".join(dns.ns_records) if dns.ns_records else "-"
    )

    table.add_row(
        "TXT",
        ", ".join(dns.txt_records) if dns.txt_records else "-"
    )

    table.add_row(
        "CNAME",
        dns.cname or "-"
    )

    console.print(table)
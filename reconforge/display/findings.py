from rich.console import Console
from rich.table import Table
from rich.text import Text

from reconforge.models.target import Target
from reconforge.models.finding_severity import FindingSeverity

console = Console()


def severity_text(severity: FindingSeverity) -> Text:
    match severity:
        case FindingSeverity.INFO:
            return Text("INFO", style="cyan")

        case FindingSeverity.LOW:
            return Text("LOW", style="green")

        case FindingSeverity.MEDIUM:
            return Text("MEDIUM", style="yellow")

        case _:
            return Text(str(severity))


def display_findings(target: Target) -> None:
    findings = target.results.findings

    if not findings:
        return

    table = Table(title="Assessment Findings")

    table.add_column("Severity", style="bold")
    table.add_column("Finding")
    table.add_column("Recommendation")

    for finding in findings:
        table.add_row(
            severity_text(finding.severity),
            f"{finding.title}\n{finding.description}",
            finding.recommendation,
        )

    console.print(table)
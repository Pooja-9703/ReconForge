import typer

from reconforge import __version__
from reconforge.core.orchestrator import ScanOrchestrator
from reconforge.exporters.json_exporter import JSONExporter

app = typer.Typer(
    help=f"ReconForge v{__version__}",
    add_completion=False,
)


@app.callback()
def main() -> None:
    """ReconForge CLI."""


@app.command()
def scan(
    target: str,
    json_output: str | None = typer.Option(
        None,
        "--json",
        help="Export scan results to a JSON file.",
    ),
) -> None:
    """
    Scan a target.
    """

    orchestrator = ScanOrchestrator()

    scan_target = orchestrator.run(target)

    if json_output:
        JSONExporter.export(scan_target, json_output)
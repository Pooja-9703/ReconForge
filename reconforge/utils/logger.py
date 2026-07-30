from rich.console import Console

console = Console()


class Logger:
    """Simple console logger."""

    @staticmethod
    def info(message: str) -> None:
        console.print(f"[cyan][*][/cyan] {message}")

    @staticmethod
    def success(message: str) -> None:
        console.print(f"[green][+][/green] {message}")

    @staticmethod
    def warning(message: str) -> None:
        console.print(f"[yellow][!][/yellow] {message}")

    @staticmethod
    def error(message: str) -> None:
        console.print(f"[red][-][/red] {message}")
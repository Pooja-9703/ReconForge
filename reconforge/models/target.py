from dataclasses import dataclass, field

from reconforge.models.results import ScanResults


@dataclass(slots=True)
class Target:
    """
    Represents a validated scan target.
    """

    original: str

    hostname: str | None = None

    ip: str | None = None

    scheme: str | None = None

    port: int | None = None

    target_type: str = "unknown"

    results: ScanResults = field(default_factory=ScanResults)
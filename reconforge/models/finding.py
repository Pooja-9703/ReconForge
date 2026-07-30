from dataclasses import dataclass

from reconforge.models.finding_severity import FindingSeverity


@dataclass(slots=True)
class Finding:
    """
    Represents an evidence-based assessment finding.
    """

    severity: FindingSeverity

    title: str
    description: str

    evidence: str

    recommendation: str
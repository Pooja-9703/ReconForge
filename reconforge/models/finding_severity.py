from enum import Enum


class FindingSeverity(str, Enum):
    """
    Severity levels for ReconForge findings.
    """

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
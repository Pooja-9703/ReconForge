class ReconForgeError(Exception):
    """Base exception for ReconForge."""


class InvalidTargetError(ReconForgeError):
    """Raised when the supplied target is invalid."""
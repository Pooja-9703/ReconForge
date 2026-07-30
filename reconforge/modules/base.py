from abc import ABC, abstractmethod

from reconforge.models.target import Target


class ReconModule(ABC):
    """
    Base class for all ReconForge modules.
    """

    name: str

    @abstractmethod
    def run(self, target: Target) -> None:
        """
        Execute the module.
        """
        raise NotImplementedError
from abc import ABC, abstractmethod

from reconforge.models.finding import Finding
from reconforge.models.target import Target


class FindingRule(ABC):
    @abstractmethod
    def analyze(self, target: Target) -> list[Finding]:
        raise NotImplementedError
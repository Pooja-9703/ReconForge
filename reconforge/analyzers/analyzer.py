from reconforge.analyzers.rules import (
    certificate,
    dns,
    http,
    ports,
    technology,
    tls,
    whois,
)
from reconforge.models.finding import Finding
from reconforge.models.target import Target

RULES = [
    tls.analyze,
    certificate.analyze,
    ports.analyze,
    http.analyze,
    dns.analyze,
    whois.analyze,
    technology.analyze,
]

class FindingAnalyzer:
    @staticmethod
    def analyze(target: Target) -> list[Finding]:
        findings: list[Finding] = []

        for rule in RULES:
            findings.extend(rule(target))

        return findings
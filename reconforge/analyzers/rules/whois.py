from datetime import datetime

from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    whois = target.results.whois

    if whois.registrar:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Registrar Identified",
                description=f"Domain registrar: {whois.registrar}",
                recommendation="Verify the registrar matches expectations.",
            )
        )

    if whois.expiration_date:
        try:
            expiry = datetime.fromisoformat(whois.expiration_date)
            remaining = (expiry - datetime.now(expiry.tzinfo)).days

            if remaining < 0:
                findings.append(
                    Finding(
                        severity=FindingSeverity.MEDIUM,
                        title="Domain Registration Expired",
                        description="The domain registration has expired.",
                        recommendation="Renew the domain registration immediately.",
                    )
                )

            elif remaining < 30:
                findings.append(
                    Finding(
                        severity=FindingSeverity.LOW,
                        title="Domain Expiring Soon",
                        description=f"The domain expires in {remaining} days.",
                        recommendation="Plan to renew the domain before expiration.",
                    )
                )

            else:
                findings.append(
                    Finding(
                        severity=FindingSeverity.INFO,
                        title="Domain Registration Active",
                        description=f"The domain is registered for another {remaining} days.",
                        recommendation="Continue monitoring renewal dates.",
                    )
                )

        except ValueError:
            pass

    if len(whois.name_servers) >= 2:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Multiple Name Servers",
                description=f"{len(whois.name_servers)} authoritative name servers are configured.",
                recommendation="Continue maintaining DNS redundancy.",
            )
        )

    return findings
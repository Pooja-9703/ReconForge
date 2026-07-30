from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    tls = target.results.tls

    if tls.days_remaining is None:
        return findings

    if tls.days_remaining >= 90:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Certificate Valid",
                description=(
                    f"The TLS certificate is valid for another "
                    f"{tls.days_remaining} days."
                ),
                recommendation="Continue monitoring certificate expiration.",
            )
        )

    elif 30 <= tls.days_remaining < 90:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Certificate Renewal Approaching",
                description=(
                    f"The TLS certificate expires in "
                    f"{tls.days_remaining} days."
                ),
                recommendation="Plan certificate renewal before expiration.",
            )
        )

    elif 0 <= tls.days_remaining < 30:
        findings.append(
            Finding(
                severity=FindingSeverity.LOW,
                title="Certificate Near Expiration",
                description=(
                    f"The TLS certificate expires in "
                    f"{tls.days_remaining} days."
                ),
                recommendation="Renew the certificate soon.",
            )
        )

    else:
        findings.append(
            Finding(
                severity=FindingSeverity.MEDIUM,
                title="Certificate Expired",
                description="The TLS certificate has expired.",
                recommendation="Replace the expired certificate immediately.",
            )
        )

    if tls.issuer:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Certificate Issuer Identified",
                description=f"Issued by: {tls.issuer}",
                recommendation="Verify the issuer matches expectations.",
            )
        )

    return findings
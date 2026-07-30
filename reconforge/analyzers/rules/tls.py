from reconforge.models.finding import Finding
from reconforge.models.target import Target
from reconforge.models.finding_severity import FindingSeverity

def analyze(target: Target) -> list[Finding]:
    """
    Analyze TLS-related observations.
    """

    findings: list[Finding] = []

    tls = target.results.tls

    if tls.tls_version is None:
        return findings

    findings.append(
        Finding(
            severity=FindingSeverity.INFO,
            title="HTTPS Enabled",
            description="The target supports HTTPS connections.",
            recommendation="Continue using HTTPS to protect communications.",
        )
    )

    if tls.tls_version == "TLSv1.3":
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Modern TLS Version",
                description="The server supports TLS 1.3.",
                recommendation="Continue using TLS 1.3 where possible.",
            )
        )

    return findings
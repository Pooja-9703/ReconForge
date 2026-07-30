from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    dns = target.results.dns

    if dns.a_records:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="IPv4 Connectivity",
                description="The target has IPv4 DNS records.",
                recommendation="No action required.",
            )
        )

    if dns.aaaa_records:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="IPv6 Supported",
                description="The target publishes IPv6 DNS records.",
                recommendation="Continue maintaining IPv6 connectivity.",
            )
        )

    if dns.mx_records:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Mail Infrastructure Detected",
                description="MX records are configured.",
                recommendation="Ensure mail infrastructure is monitored and maintained.",
            )
        )

    if dns.txt_records:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="TXT Records Present",
                description="The domain publishes TXT records.",
                recommendation="Review TXT records periodically for accuracy.",
            )
        )

    if len(dns.ns_records) >= 2:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Redundant Name Servers",
                description=f"{len(dns.ns_records)} authoritative name servers were detected.",
                recommendation="Continue maintaining DNS redundancy.",
            )
        )

    return findings
from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    ports = target.results.ports.open_ports

    if not ports:
        return findings

    port_numbers = {port.port for port in ports}

    if 21 in port_numbers:
        findings.append(
            Finding(
                severity=FindingSeverity.LOW,
                title="FTP Service Exposed",
                description="An FTP service was detected.",
                evidence="Port 21 responded during the port scan.",
                recommendation="Disable FTP if unnecessary or migrate to SFTP/FTPS.",
            )
        )

    if 443 in port_numbers:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="HTTPS Service Detected",
                description="The target exposes an HTTPS service.",
                recommendation="Continue using HTTPS for encrypted communication.",
            )
        )

    if 8080 in port_numbers:
        findings.append(
            Finding(
                severity=FindingSeverity.INFO,
                title="Alternative HTTP Port",
                description="An HTTP service is running on port 8080.",
                recommendation="Verify that this service is intended to be publicly accessible.",
            )
        )

    if len(port_numbers) >= 4:
        findings.append(
            Finding(
                severity=FindingSeverity.LOW,
                title="Multiple Public Services",
                description=f"{len(port_numbers)} public services were detected.",
                recommendation="Review exposed services and disable any that are unnecessary.",
            )
        )

    return findings
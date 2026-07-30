from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    technologies = target.results.technology.technologies

    if not technologies:
        return findings

    findings.append(
        Finding(
            severity=FindingSeverity.INFO,
            title="Technology Fingerprinting Complete",
            description=f"{len(technologies)} technologies were identified.",
            recommendation="Review detected technologies for inventory and maintenance.",
        )
    )

    security_products = {
        "cloudflare",
        "akamai",
        "fastly",
        "imperva",
        "sucuri",
    }

    for technology in technologies:
        if technology.lower() in security_products:
            findings.append(
                Finding(
                    severity=FindingSeverity.INFO,
                    title="Edge Protection Detected",
                    description=f"{technology} appears to protect the application.",
                    recommendation="Verify the edge protection configuration is kept up to date.",
                )
            )

    web_servers = {
        "nginx",
        "apache",
        "iis",
        "caddy",
    }

    for technology in technologies:
        if technology.lower() in web_servers:
            findings.append(
                Finding(
                    severity=FindingSeverity.INFO,
                    title="Web Server Identified",
                    description=f"{technology} was detected.",
                    recommendation="Keep the web server updated and properly configured.",
                )
            )

    return findings
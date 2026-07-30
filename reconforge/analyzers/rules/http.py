from reconforge.models.finding import Finding
from reconforge.models.finding_severity import FindingSeverity
from reconforge.models.target import Target


def analyze(target: Target) -> list[Finding]:
    findings: list[Finding] = []

    headers = {
        key.lower(): value
        for key, value in target.results.http.headers.items()
    }

    if not headers:
        return findings

    recommended_headers = {
        "strict-transport-security": (
            "HSTS Enabled",
            "HTTP Strict Transport Security is configured.",
            "Continue using HSTS to enforce HTTPS.",
        ),
        "content-security-policy": (
            "Content Security Policy Present",
            "A Content Security Policy header is configured.",
            "Review the policy regularly to keep it effective.",
        ),
        "x-frame-options": (
            "Clickjacking Protection Enabled",
            "The X-Frame-Options header is present.",
            "Continue using clickjacking protection.",
        ),
        "x-content-type-options": (
            "MIME Sniffing Protection Enabled",
            "The X-Content-Type-Options header is present.",
            "Keep MIME sniffing protection enabled.",
        ),
        "referrer-policy": (
            "Referrer Policy Configured",
            "A Referrer-Policy header is configured.",
            "Review the policy to ensure it matches your privacy requirements.",
        ),
    }

    for header, (title, description, recommendation) in recommended_headers.items():
        if header in headers:
            findings.append(
                Finding(
                    severity=FindingSeverity.INFO,
                    title=title,
                    description=description,
                    recommendation=recommendation,
                )
            )

    return findings
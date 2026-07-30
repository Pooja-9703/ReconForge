from urllib.parse import urlparse
import ipaddress

from reconforge.models.target import Target
from reconforge.core.exceptions import InvalidTargetError


class TargetValidator:
    """
    Validates and normalizes scan targets.
    """

    def validate(self, raw_target: str) -> Target:
        raw_target = raw_target.strip()

        if not raw_target:
            raise InvalidTargetError("Target cannot be empty.")

        # URL
        if raw_target.startswith(("http://", "https://")):
            parsed = urlparse(raw_target)

            # Use explicit port if provided, otherwise infer the default.
            if parsed.port is not None:
                port = parsed.port
            elif parsed.scheme == "http":
                port = 80
            elif parsed.scheme == "https":
                port = 443
            else:
                port = None

            return Target(
                original=raw_target,
                hostname=parsed.hostname,
                scheme=parsed.scheme,
                port=port,
                target_type="url",
            )

        # IP
        try:
            ipaddress.ip_address(raw_target)

            return Target(
                original=raw_target,
                ip=raw_target,
                target_type="ip",
            )

        except ValueError:
            pass

        # Domain
        return Target(
            original=raw_target,
            hostname=raw_target,
            target_type="domain",
        )
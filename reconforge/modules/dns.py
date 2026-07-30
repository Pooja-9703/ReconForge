import socket

import dns.resolver

from reconforge.models.target import Target
from reconforge.modules.base import ReconModule
from reconforge.utils.logger import Logger


class DNSResolver(ReconModule):
    """
    Resolve hostnames and enumerate DNS records.
    """

    name = "DNS Resolver"

    RECORD_MAPPINGS = {
        "A": "a_records",
        "AAAA": "aaaa_records",
        "MX": "mx_records",
        "NS": "ns_records",
        "TXT": "txt_records",
    }

    def resolve_records(
        self,
        hostname: str,
        record_type: str,
    ) -> list[str]:
        """
        Resolve a DNS record type.
        """

        try:
            answers = dns.resolver.resolve(hostname, record_type)

            return [str(answer).rstrip(".") for answer in answers]

        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.resolver.LifetimeTimeout,
        ):
            return []

    def run(self, target: Target) -> None:

        if not target.hostname:
            Logger.warning("No hostname to resolve.")
            return

        try:
            target.ip = socket.gethostbyname(target.hostname)
            target.results.dns.resolved_ip = target.ip

            Logger.success(f"Resolved IP: {target.ip}")

        except socket.gaierror:
            Logger.warning("Unable to resolve hostname.")
            return

        dns_results = target.results.dns

        for record_type, attribute in self.RECORD_MAPPINGS.items():
            setattr(
                dns_results,
                attribute,
                self.resolve_records(target.hostname, record_type),
            )

        cname = self.resolve_records(
            target.hostname,
            "CNAME",
        )

        dns_results.cname = cname[0] if cname else None

        Logger.success("DNS enumeration complete.")
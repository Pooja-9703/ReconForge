import socket
import ssl
from datetime import datetime, UTC

from reconforge.models.target import Target
from reconforge.modules.base import ReconModule
from reconforge.utils.logger import Logger


class TLSModule(ReconModule):
    """
    Collect TLS certificate information from HTTPS targets.
    """

    name = "TLS Module"

    def run(self, target: Target) -> None:

        if target.scheme != "https":
            Logger.info("Skipping TLS inspection (non-HTTPS target).")
            return

        try:
            context = ssl.create_default_context()

            with socket.create_connection(
                (target.hostname, target.port),
                timeout=5,
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=target.hostname,
                ) as tls_sock:

                    cert = tls_sock.getpeercert()

                    tls = target.results.tls

                    tls.tls_version = tls_sock.version()

                    cipher = tls_sock.cipher()
                    tls.cipher = cipher[0] if cipher else None

                    subject = dict(
                        x[0] for x in cert.get("subject", [])
                    )

                    issuer = dict(
                        x[0] for x in cert.get("issuer", [])
                    )

                    tls.subject = subject.get("commonName")
                    tls.issuer = issuer.get("commonName")

                    not_before = cert.get("notBefore")
                    not_after = cert.get("notAfter")

                    if not_before:
                        valid_from = datetime.strptime(
                            not_before,
                            "%b %d %H:%M:%S %Y %Z",
                        )
                        tls.valid_from = valid_from.strftime("%Y-%m-%d %H:%M:%S UTC")

                    if not_after:
                        valid_until = datetime.strptime(
                            not_after,
                            "%b %d %H:%M:%S %Y %Z",
                        )
                        tls.valid_until = valid_until.strftime("%Y-%m-%d %H:%M:%S UTC")

                        remaining = (
                            valid_until.replace(tzinfo=UTC)
                            - datetime.now(UTC)
                        )

                        tls.days_remaining = remaining.days
                    
                    tls.sans = [
                        value
                        for record_type, value in cert.get("subjectAltName", [])
                        if record_type == "DNS"
                    ]

                    Logger.success("TLS information collected.")

        except ssl.SSLError as e:
            Logger.warning(f"TLS error: {e}")

        except socket.timeout:
            Logger.warning("TLS connection timed out.")

        except socket.gaierror:
            Logger.warning("Unable to resolve host for TLS inspection.")

        except ConnectionRefusedError:
            Logger.warning("TLS connection refused.")

        except Exception as e:
            Logger.warning(f"Unexpected TLS error: {e}")
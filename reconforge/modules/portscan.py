import socket
from concurrent.futures import ThreadPoolExecutor

from reconforge.models.results import PortInfo
from reconforge.models.target import Target
from reconforge.modules.base import ReconModule
from reconforge.utils.logger import Logger


class PortScanner(ReconModule):
    """
    Scan common TCP ports on a target.
    """

    name = "Port Scanner"

    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        6379: "Redis",
        8080: "HTTP-Alt",
    }

    def scan_port(
        self,
        ip: str,
        port: int,
        service: str,
    ) -> PortInfo | None:

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)

                if sock.connect_ex((ip, port)) == 0:
                    banner = self.grab_banner(ip,port)

                    return PortInfo(
                        port=port,
                        service=service,
                        banner=banner,
                    )

        except OSError:
            pass

        return None

    def run(self, target: Target) -> None:

        if target.ip is None:
            Logger.warning("Port scan skipped (no resolved IP).")
            return

        Logger.info("Scanning common TCP ports...")

        open_ports = []

        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [
                executor.submit(
                    self.scan_port,
                    target.ip,
                    port,
                    service,
                )
                for port, service in self.COMMON_PORTS.items()
            ]

            for future in futures:

                result = future.result()

                if result is not None:
                    open_ports.append(result)

        open_ports.sort(key=lambda p: p.port)

        target.results.ports.open_ports = open_ports

        Logger.success(f"Found {len(open_ports)} open port(s).")

    def grab_banner(
        self,
        ip: str,
        port: int,
    ) -> str | None:

        try:
            with socket.create_connection((ip, port), timeout=1) as sock:
                sock.settimeout(1)

                try:
                    banner = sock.recv(1024)

                    if banner:
                        return banner.decode(
                            errors="ignore"
                        ).strip()

                except socket.timeout:
                    return None

        except OSError:
            return None

        return None
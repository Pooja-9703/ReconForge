from rich.console import Console
from rich.table import Table

from reconforge.display.target import display_target
from reconforge.display.dns import display_dns
from reconforge.display.http import display_http
from reconforge.display.tls import display_tls
from reconforge.display.ports import display_ports
from reconforge.display.whois import display_whois
from reconforge.display.technology import display_technology

from reconforge.models.target import Target
from reconforge.validators.target_validator import TargetValidator
from reconforge.modules.dns import DNSResolver
from reconforge.utils.logger import Logger
from reconforge.modules.http import HTTPModule
from reconforge.modules.tls import TLSModule
from reconforge.modules.portscan import PortScanner
from reconforge.modules.whois import WHOISModule
from reconforge.modules.technology import TechnologyModule

console = Console()


class ScanOrchestrator:
    """
    Coordinates the scanning workflow.
    """

    def __init__(self) -> None:
        self.validator = TargetValidator()
        self.modules = [
            DNSResolver(),
            HTTPModule(),
            TLSModule(),
            PortScanner(),
            WHOISModule(),
            TechnologyModule(),
        ]

    def run(self, raw_target: str) -> Target:
        target = self.validator.validate(raw_target)

        for module in self.modules:
            Logger.info(f"Running {module.name}...")
            module.run(target)

        console.rule("[bold cyan]ReconForge")

        display_target(target)
        display_dns(target)
        display_http(target)
        display_tls(target)
        display_ports(target)
        display_whois(target)
        display_technology(target)
        
        Logger.success("Validation complete.")
        return target
import whois

from reconforge.modules.base import ReconModule
from reconforge.models.target import Target
from reconforge.utils.logger import Logger


class WHOISModule(ReconModule):
    name = "WHOIS Module"

    def run(self, target: Target) -> None:
        if not target.hostname:
            Logger.warning("No hostname available for WHOIS lookup.")
            return

        try:
            data = whois.whois(target.hostname)

            result = target.results.whois

            result.registrar = self._to_string(data.registrar)
            result.creation_date = self._to_string(data.creation_date)
            result.expiration_date = self._to_string(data.expiration_date)
            result.updated_date = self._to_string(data.updated_date)
            result.name_servers = self._to_list(data.name_servers)

            Logger.success("WHOIS information collected.")

        except Exception as e:
            Logger.warning(f"WHOIS lookup failed: {e}")

    @staticmethod
    def _to_string(value) -> str | None:
        if value is None:
            return None

        if isinstance(value, list):
            value = value[0]

        return str(value)

    @staticmethod
    def _to_list(value) -> list[str]:
        if value is None:
            return []

        if isinstance(value, list):
            return [str(v) for v in value]

        return [str(value)]
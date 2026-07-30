import json
from dataclasses import asdict
from pathlib import Path

from reconforge.models.target import Target
from reconforge.utils.logger import Logger


class JSONExporter:
    """
    Export scan results to a JSON file.
    """

    @staticmethod
    def export(target: Target, output_file: str) -> None:
        """
        Export the target and scan results to a JSON file.
        """

        data = {
            "target": {
                "original": target.original,
                "target_type": target.target_type,
                "hostname": target.hostname,
                "scheme": target.scheme,
                "port": target.port,
            },
            "results": asdict(target.results),
        }

        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        Logger.success(f"JSON report saved to {path}")
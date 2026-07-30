import httpx

from reconforge.modules.base import ReconModule
from reconforge.models.target import Target
from reconforge.utils.logger import Logger


class TechnologyModule(ReconModule):
    name = "Technology Fingerprinting"

    def run(self, target: Target) -> None:
        if not target.hostname:
            Logger.warning("No hostname available for technology fingerprinting.")
            return

        url = f"{target.scheme}://{target.hostname}"

        try:
            response = httpx.get(
                url,
                timeout=10,
                follow_redirects=True,
            )

            html = response.text.lower()
            headers = response.headers

            technologies = set()

            self._detect_server(headers, technologies)
            self._detect_powered_by(headers, technologies)
            self._detect_html(html, technologies)

            target.results.technology.technologies = sorted(technologies)

            Logger.success("Technology fingerprinting complete.")

        except Exception as e:
            Logger.warning(f"Technology fingerprinting failed: {e}")

    @staticmethod
    def _detect_server(headers, technologies: set[str]) -> None:
        server = headers.get("server", "").lower()

        if "nginx" in server:
            technologies.add("Nginx")

        if "apache" in server:
            technologies.add("Apache")

        if "cloudflare" in server:
            technologies.add("Cloudflare")

        if "iis" in server:
            technologies.add("Microsoft IIS")

    @staticmethod
    def _detect_powered_by(headers, technologies: set[str]) -> None:
        powered = headers.get("x-powered-by", "").lower()

        if "php" in powered:
            technologies.add("PHP")

        if "express" in powered:
            technologies.add("Express")

        if "asp.net" in powered:
            technologies.add("ASP.NET")

    @staticmethod
    def _detect_html(html: str, technologies: set[str]) -> None:
        if "wp-content" in html:
            technologies.add("WordPress")

        if "bootstrap" in html:
            technologies.add("Bootstrap")

        if "jquery" in html:
            technologies.add("jQuery")

        if "react" in html:
            technologies.add("React")

        if "vue" in html:
            technologies.add("Vue.js")

        if "angular" in html:
            technologies.add("Angular")

        if "googletagmanager" in html:
            technologies.add("Google Tag Manager")

        if "google-analytics" in html:
            technologies.add("Google Analytics")
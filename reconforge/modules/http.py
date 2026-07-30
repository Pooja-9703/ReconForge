import time

import httpx

from reconforge.models.target import Target
from reconforge.modules.base import ReconModule
from reconforge.utils.logger import Logger

class HTTPModule(ReconModule):
    """
    Collect HTTP information about a target.
    """

    name = "HTTP Module"

    def extract_title(self, html: str) -> str | None:
        """
        Extract the HTML <title> tag.
        """

        lower = html.lower()

        start = lower.find("<title>")
        end = lower.find("</title>")

        if start == -1 or end == -1:
            return None

        return html[start + 7:end].strip()

    def run(self, target: Target) -> None:

        if target.target_type != "url":
            Logger.warning("HTTP module skipped (target is not a URL).")
            return

        try:
            start = time.perf_counter()

            with httpx.Client(
                follow_redirects=True,
                timeout=10,
            ) as client:

                response = client.get(target.original)

            elapsed = (time.perf_counter() - start) * 1000

            target.results.http.status_code = response.status_code
            target.results.http.server = response.headers.get("Server")
            target.results.http.headers = {
                key: value
                for key, value in response.headers.items()
            }

            content_type = response.headers.get("Content-Type")

            target.results.http.content_type = (
                content_type.split(";")[0].strip()
                if content_type
                else None
            )

            content_length = response.headers.get("Content-Length")
            target.results.http.content_length = (
                int(content_length)
                if content_length and content_length.isdigit()
                else None
            )

            target.results.http.redirect_url = (
                str(response.url)
                if str(response.url) != target.original
                else None   
            )

            target.results.http.title = self.extract_title(response.text)

            target.results.http.response_time = round(elapsed, 2)

            Logger.success("HTTP information collected.")

        except httpx.HTTPError as e:
            Logger.warning(f"HTTP request failed: {e}")

        
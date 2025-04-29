"""Gathers IPs known to be used by Fastly services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class Fastly(BaseService):
    """Fastly IPs service."""

    HOST = "https://api.fastly.com"
    ENDPOINT = "/public-ip-list"

    def parse_response(self, response):
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        source = Source(
            name="Fastly",
            url=self.get_url(),
        )
        response = response.json()
        source.add_service(
            name="Fastly",
            ips=response["addresses"],
        )
        return source

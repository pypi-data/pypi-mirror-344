"""Gathers IPs known to be used by Box services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class Box(BaseService):
    """Box IPs service."""

    HOST = "https://box.zendesk.com"
    ENDPOINT = "/ips"

    def parse_response(self, response):
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        source = Source(
            name="Box",
            url=self.get_url(),
        )
        response = response.json()
        source.add_service(
                name="Box",
                ips=response["ips"]["ingress"]["all"],
            )
        return source

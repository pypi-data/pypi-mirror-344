"""Gathers IPs known to be used by O365 services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class O365(BaseService):
    """O365 IPs service."""

    HOST = "https://endpoints.office.com"
    ENDPOINT = "/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7"

    def parse_response(self, response):
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        source = Source(
            name="O365",
            url=self.get_url(),
        )
        response = response.json()
        for service in response:
            source.add_service(
                name=service["serviceAreaDisplayName"],
                ips=service["ips"] if service.get("ips") else [],
            )
        return source

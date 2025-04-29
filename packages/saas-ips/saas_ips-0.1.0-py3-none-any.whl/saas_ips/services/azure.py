"""Gathers IPs known to be used by Azure services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class Azure(BaseService):
    """Azure IPs service."""

    HOST = "https://download.microsoft.com"
    ENDPOINT = "download/7/1/d/71d86715-5596-4529-9b13-da13a5de5b63/ServiceTags_Public_20250421.json"

    def parse_response(self, response):
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        source = Source(
            name="Azure",
            url=self.get_url(),
        )
        response = response.json()
        for service in response["values"]:
            if service["properties"]["changeNumber"] > 0:
                source.add_service(
                    name=service["properties"]["systemService"] if service["properties"]["systemService"] else service["name"],
                    ips=service["properties"]["addressPrefixes"],
                    region=service["properties"]["region"],
                )
        return source

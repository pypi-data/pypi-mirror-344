"""Gathers IPs known to be used by Google services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class Google(BaseService):
    """Google IPs service."""

    HOST = "https://www.gstatic.com/ipranges/"

    def run(self):
        """Run the service."""
        return_list: list = []
        for endpoint in ["goog.json", "cloud.json"]:
            self.ENDPOINT = endpoint
            res = self._run()
            return_list.append(self.parse_response(res))
        return return_list

    def parse_response(self, response) -> Source:
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        service_name: str = ""
        if response.url.endswith("goog.json"):
            service_name = "Google"
        elif response.url.endswith("cloud.json"):
            service_name = "Google Cloud"
        source = Source(
            name=service_name,
            url=self.get_url(),
        )
        response = response.json()
        if response.get("prefixes"):
            for item in response.get("prefixes"):
                source.add_service(
                    name=item["service"] if item.get("service") else service_name,
                    ips=item["ipv4Prefix"] if item.get("ipv4Prefix") else [],
                    region=item["scope"] if item.get("scope") else None,
                )
        return source

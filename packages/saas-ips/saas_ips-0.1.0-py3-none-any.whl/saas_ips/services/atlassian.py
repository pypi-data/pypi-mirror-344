"""Gathers IPs known to be used by Atlassian services."""
from saas_ips.services.base import BaseService
from saas_ips.models import Source


class Atlassian(BaseService):
    """Atlassian IPs service."""

    HOST = "https://ip-ranges.atlassian.com/"

    def parse_response(self, response) -> Source:
        """Parse the response."""
        self.__logger.debug(f"Parsing response from {self.get_url()}.")
        source = Source(
            name="Atlassian",
            url=self.HOST,
        )
        product_dict: dict = {}
        response = response.json()
        if response.get("items"):
            for item in response.get("items"):
                if item.get("product") and len(item.get("product")) > 0:
                    for product in item.get("product"):
                        if product not in product_dict:
                            product_dict[product] = []
                        if item.get("network"):
                            source.add_service(
                                name=product,
                                ips=item["network"],
                                region=item.get("region"),
                            )
        return source

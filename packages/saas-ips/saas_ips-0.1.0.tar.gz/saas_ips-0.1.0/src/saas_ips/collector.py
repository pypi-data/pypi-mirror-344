"""The main entrypoint for the SaaS Data Collector."""
import json
import os
from datetime import datetime
from typing import Optional

from attrs import asdict

from saas_ips.base import Base
from saas_ips.services import Atlassian, Azure, Box, Fastly, Google, O365 # type: ignore
from saas_ips.models import KnownIPs, Source


def serialize(inst, field, value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value


class Collector(Base):
    """Collector class."""

    def _write_output(self, known: KnownIPs, output: str) -> None:
        """Write the output to a file."""
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))
        with open(output, "w") as file:
            json.dump(asdict(known, value_serializer=serialize), file, indent=4)

    def run(self, output: Optional[str] = "") -> KnownIPs:
        """Run the collector."""
        known = KnownIPs()
        self.__logger.info("Running the collector.")
        for service in [Atlassian, Azure, Box, Fastly, Google, O365]:
            res = service().run()
            if isinstance(res, list):
                for item in res:
                    if isinstance(item, Source):
                        known.sources.append(item)
            else:
                known.sources.append(res)

        if output:
            self._write_output(known, output)

        self.__logger.info("Collector finished.")
        return known.sources

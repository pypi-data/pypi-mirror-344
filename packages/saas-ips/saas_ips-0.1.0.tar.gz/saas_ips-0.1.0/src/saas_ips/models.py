"""Contains main response models for the SaaS Data Collector."""
import ipaddress
from datetime import datetime
from typing import List, Optional

from attrs import define, field


@define
class IP:
    ip: str = field(metadata={"description": "The IP address."})
    region: Optional[str] = field(default=None, metadata={"description": "The region the IP address is located."})

    @ip.validator
    def validate_ip(self, attribute, value):
        """Validates the IP address."""
        try:
            ip = ipaddress.IPv4Network(value)
        except ValueError:
            try:
                ip = ipaddress.IPv6Network(value)
            except ValueError:  
                raise ValueError(f"The IP address '{value}' is invalid.")
        except Exception as e:
            raise e


@define
class Service:
    name: str = field(metadata={"description": "The name of the service."})
    ips: List[IP] = field(factory=list, metadata={"description": "The list of known IPs for the service."})


@define
class Source:
    name: str = field(metadata={"description": "The name of the source."})
    url: str = field(metadata={"description": "The URL of the source."})
    services: List[Service] = field(factory=list, metadata={"description": "The list of services and their known IPs."})

    def add_service(self, name: str, ips: str, region: Optional[str] = None) -> None:
        """Add a service to the source."""
        if not self.services:
            self.services = []
        for service in self.services:
            if service.name == name:
                if isinstance(ips, list):
                    for ip in ips:
                        service.ips.append(IP(ip=ip, region=region))
                else:
                    service.ips.append(IP(ip=ips, region=region))
                return
        if isinstance(ips, list):
            self.services.append(Service(name=name, ips=[IP(ip=ip, region=region) for ip in ips]))
        else:
            self.services.append(Service(name=name, ips=[IP(ip=ips, region=region)]))


@define
class KnownIPs:
    last_updated: datetime = field(default=datetime.now(), metadata={"description": "The last time the data was updated."})
    sources: List[Source] = field(factory=list, metadata={"description": "The list of sources and their known IPs."})

"""The base service class."""
import abc

from enum import Enum
from typing import Optional, Dict, Any
from urllib.parse import urljoin

import requests

from saas_ips.base import Base
from saas_ips.models import Source


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseService(Base):

    HEADERS = {'Content-Type': 'application/json'}
    METHOD: Method = Method.GET
    HOST: str = ""
    ENDPOINT: str = ""
    KWARGS: Dict = {}
    _session: requests.Session = requests.Session()

    def __init__(self, proxy: Optional[Dict[str, str]] = None, verify: bool = True, raise_for_status: bool = True):
        if proxy:
            self._session.proxies = {
                "http": proxy,
                "https": proxy
            }
        self.raise_for_status = raise_for_status
        self._session.headers.update(self.HEADERS)
        self._session.verify = verify

    def get_url(self) -> str:
        return urljoin(self.HOST, self.ENDPOINT)

    def _run(self) -> requests.Response:
        try:
            self.__logger.info(f'Sending {self.METHOD} request to {self.get_url()}')
            response = self._session.request(
                method=self.METHOD.value,
                url=self.get_url(),
                **self.KWARGS
            )
            if self.raise_for_status:
                response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as errh:
            self.__logger.error("An Http Error occurred: " + repr(errh))
        except requests.exceptions.ConnectionError as errc:
            self.__logger.error("An Error Connecting to the API occurred: " + repr(errc))
        except requests.exceptions.Timeout as errt:
            self.__logger.error("A Timeout Error occurred: " + repr(errt))
        except requests.exceptions.RequestException as err:
            self.__logger.error("An Unknown Error occurred: " + repr(err))

    def run(self) -> Any:
        self.__logger.debug(f"Running {self.__class__.__name__}")
        return self.parse_response(self._run())

    @abc.abstractmethod
    def parse_response(self) -> Source:
        raise NotImplemented

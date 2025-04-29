"""The base class for all services and endpoints.

All classes should inherit from this class.
"""
from saas_ips.logger import LoggingBase


class Base(metaclass=LoggingBase):
    _TEST = None

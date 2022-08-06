"""Implements in-memory storage"""

from ipaddress import IPv4Address
from typing import Optional


class SubdomainTable:
    """Implements size limited (key, value) subdomains storage"""

    def __init__(self, max_size: int = 128):
        """
        Init table with records storage (as list) limited by size
        :param max_size: max size of records to store
        """
        self._records: list[tuple[str, IPv4Address]] = []
        self._size = max_size

    def add(self, subdomain: str, ip: IPv4Address) -> None:
        """
        Add record to the storage
        :param subdomain: subdomain as key
        :param ip: required IPv4 as value
        :return: None
        """
        if len(self._records) >= self._size:
            # remove first (oldest) record from the list
            self._records.pop(0)

        record = (subdomain, ip)

        if record in self._records:
            return

        self._records.append(record)

    def get(self, subdomain: str) -> Optional[IPv4Address]:
        """
        Get record from the storage
        :param subdomain: subdomain as key
        :return: IPv4 if record found, None otherwise
        """
        for record in self._records:
            rec_subdomain, rec_ip = record
            if subdomain == rec_subdomain:
                return rec_ip

        return None

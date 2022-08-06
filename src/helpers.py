"""Implements set of helper functions"""

import random
import socket
import struct
from functools import cache
from ipaddress import IPv4Address


def get_random_ip_v4() -> IPv4Address:
    """
    Generates random IPv4 address
    :return: IPv4 address as string
    """
    ip_raw: str = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))

    return IPv4Address(ip_raw)


@cache
def parse_ip(query_ip: str) -> IPv4Address:
    """
    Parse IP representation from query
    :param query_ip: IPv4 represented as "%d-%d-%d-%d" (note "-" instead of ".")
    :return: IPv4 as IPv4Address
    """
    ip_raw: str = query_ip.replace("-", ".")

    return IPv4Address(ip_raw)

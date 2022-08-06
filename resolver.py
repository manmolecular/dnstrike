#!/usr/bin/env python3
"""Start Weaponized DNStrike server"""

import time
import argparse
from dnslib.server import DNSServer, DNSLogger

from src.resolver import WeaponizedResolver

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="DNStrike: Weaponized DNS Resolver")
    p.add_argument(
        "--port",
        "-p",
        type=int,
        default=53,
        metavar="<port>",
        help="Server listen port",
    )
    p.add_argument(
        "--address",
        "-a",
        type=str,
        default="0.0.0.0",
        metavar="<address>",
        help="Server listen address",
    )
    args = p.parse_args()

    resolver = WeaponizedResolver()

    logger = DNSLogger("request,reply,truncated,error,recv,send,data", prefix=True)

    udp_server = DNSServer(
        resolver, port=args.port, address=args.address, logger=logger
    )
    udp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)

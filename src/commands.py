"""Defines supported commands for the DNS resolver"""

from enum import Enum


class Commands(str, Enum):
    """Defines supported commands"""

    # example: 1-1-1-1.bind.subdomain.domain.tld
    BIND = "bind"

    # example: random.subdomain.domain.tld
    RANDOM = "random"

    # example: subdomain.as.1-1-1-1.subdomain.domain.tld
    AS = "as"

    # example: subdomain.lookup.subdomain.domain.tld
    LOOKUP = "lookup"


SUPPORTED_COMMANDS = {command.value for command in Commands}

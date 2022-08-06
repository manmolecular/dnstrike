"""Implements Weaponized DNStrike Resolver"""

from ipaddress import IPv4Address

from dnslib import RR, DNSRecord, QTYPE, A, CLASS, DNSLabel, DNSQuestion, TXT

from src.commands import Commands, SUPPORTED_COMMANDS
from src.helpers import get_random_ip_v4, parse_ip
from src.storage import SubdomainTable


class WeaponizedResolver:
    def __init__(self, ttl: int = 60):
        """
        Init resolver
        :param ttl: time to live for the record
        """
        self.storage = SubdomainTable()
        self.ttl = ttl

    def handle_command(self, command: str, tokens: list[str]) -> IPv4Address:
        """
        Handle command from query
        :param command: one of the Commands-supported command
        :param tokens: tokens as segments between dots "." in the query name
        :return: IPv4 address
        """
        if command == Commands.BIND:
            query_ip, *_ = tokens
            ip: IPv4Address = parse_ip(query_ip)

            return ip

        elif command == Commands.RANDOM:
            ip: IPv4Address = get_random_ip_v4()

            return ip

        elif command == Commands.AS:
            query_subdomain, _, query_ip, *_ = tokens
            ip: IPv4Address = parse_ip(query_ip)

            self.storage.add(query_subdomain, ip)

            return ip

        elif command == Commands.LOOKUP:
            query_subdomain, *_ = tokens
            ip: IPv4Address = self.storage.get(query_subdomain)

            if ip is None:
                raise LookupError("no IP for the provided subdomain")

            return ip

        raise ValueError("no supported commands provided")

    def process_query(self, query_name: DNSLabel) -> IPv4Address:
        """
        Process provided query: parse it, perform command
        :param query_name: query name as DNSLabel
        :return: IPv4 address
        """
        query_str = str(query_name)
        tokens: list[str] = query_str.split(".")
        commands = list(set(tokens).intersection(SUPPORTED_COMMANDS))

        if not commands:
            raise ValueError("no supported commands provided")

        if len(commands) > 1:
            raise ValueError("only 1 command at a time is supported")

        command = commands[0]

        ip = self.handle_command(command, tokens)

        return ip

    def resolve(self, request: DNSRecord, *args, **kwargs) -> DNSRecord:  # noqa
        """
        Resolve DNS query
        :param request: DNS query as DNSRecord
        :param args: args suppressor
        :param kwargs: kwargs suppressor
        :return: None
        """
        reply = request.reply()
        query: DNSQuestion = request.q
        query_name: DNSLabel = query.qname

        try:
            ip = self.process_query(query_name)
        except (ValueError, LookupError):
            err_msg = "can not process query".encode()
            reply.add_answer(
                RR(query_name, QTYPE.TXT, ttl=self.ttl, rdata=TXT(err_msg))
            )
            return reply
        except Exception:  # noqa
            err_msg = "unexpected error".encode()
            reply.add_answer(
                RR(query_name, QTYPE.TXT, ttl=self.ttl, rdata=TXT(err_msg))
            )
            return reply

        ip_str = str(ip)

        answer = RR(
            query_name,
            ttl=self.ttl,
            rclass=CLASS.IN,
            rtype=QTYPE.A,
            rdata=A(ip_str),
        )

        reply.add_answer(answer)

        return reply

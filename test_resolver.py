import re
import unittest

from dnslib import CLASS
from dnslib.client import DNSRecord, DNSQuestion, QTYPE
from dnslib.server import DNSServer
from ipaddress import IPv4Address

from src.resolver import WeaponizedResolver
from src.storage import SubdomainTable
from src.helpers import get_random_ip_v4

DNS_PORT = 55053
DNS_HOST = "127.0.0.1"
DNS_TTL = 10


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._storage = SubdomainTable(max_size=2)

    def test_add(self):
        ip = IPv4Address("1.2.3.4")
        self._storage.add(subdomain="subdomain", ip=ip)
        assert len(self._storage._records) == 1

        # test duplicates
        self._storage.add(subdomain="subdomain", ip=ip)
        assert len(self._storage._records) == 1

    def test_max_size(self):
        self._storage.add(subdomain="subdomain-max-1", ip=get_random_ip_v4())
        self._storage.add(subdomain="subdomain-max-2", ip=get_random_ip_v4())
        self._storage.add(subdomain="subdomain-max-3", ip=get_random_ip_v4())

        assert len(self._storage._records) == 2

        assert self._storage.get("subdomain-max-1") is None
        assert self._storage.get("subdomain-max-2") is not None
        assert self._storage.get("subdomain-max-3") is not None

    def test_get(self):
        ip = get_random_ip_v4()
        self._storage.add(subdomain="subdomain-get-test", ip=ip)
        assert self._storage.get("subdomain-get-test") == ip


class TestWeaponizedResolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        resolver = WeaponizedResolver(ttl=DNS_TTL)
        udp_server = DNSServer(resolver, port=DNS_PORT, address=DNS_HOST)
        udp_server.start_thread()

        cls._resolver = resolver

    def test_bind(self):
        bind_ip_query = "11-22-33-44"
        bind_ip_expected = bind_ip_query.replace("-", ".")

        question = DNSQuestion(
            f"{bind_ip_query}.bind.localhost", qtype=QTYPE.A, qclass=CLASS.IN
        )

        record = DNSRecord(q=question)
        response = record.send(dest=DNS_HOST, port=DNS_PORT, tcp=False)
        response_parsed = DNSRecord.parse(response)

        assert bind_ip_expected in str(response_parsed.a)

    def test_random(self):
        question = DNSQuestion(f"random.localhost", qtype=QTYPE.A, qclass=CLASS.IN)

        record = DNSRecord(q=question)
        response = record.send(dest=DNS_HOST, port=DNS_PORT, tcp=False)
        response_parsed = DNSRecord.parse(response)

        ip_response = re.search(r"\d+\.\d+\.\d+\.\d+", str(response_parsed.a))
        assert ip_response

    def test_as(self):
        as_ip_query = "55-66-77-88"
        as_ip_expected = as_ip_query.replace("-", ".")

        question = DNSQuestion(
            f"unittest.as.{as_ip_query}.localhost", qtype=QTYPE.A, qclass=CLASS.IN
        )

        record = DNSRecord(q=question)
        response = record.send(dest=DNS_HOST, port=DNS_PORT, tcp=False)
        response_parsed = DNSRecord.parse(response)

        assert len(self._resolver.storage._records) == 1

        storage_record = self._resolver.storage._records[0]
        record_subdomain, record_ip = storage_record
        assert record_subdomain == "unittest"
        assert str(record_ip) == as_ip_expected

        assert as_ip_expected in str(response_parsed.a)

    def test_lookup(self):
        lookup_ip_expected = "55.66.77.88"
        question = DNSQuestion(
            f"unittest.lookup.localhost", qtype=QTYPE.A, qclass=CLASS.IN
        )

        record = DNSRecord(q=question)
        response = record.send(dest=DNS_HOST, port=DNS_PORT, tcp=False)
        response_parsed = DNSRecord.parse(response)

        assert lookup_ip_expected in str(response_parsed.a)


if __name__ == "__main__":
    unittest.main()

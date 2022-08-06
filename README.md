# dnstrike
A small set of DNS utilities in the form of a weaponized DNS resolver. Use cases: SSRF exploitation, playing with DNS, anything you want.

## Commands
 - `<ip>.bind` - resolves IPv4-like subdomain in the form of `%d-%d-%d-%d` to the IPv4 address, example: `1-1-1-1.bind.domain.tld` resolves to `1.1.1.1`
 - `random` - resolves to random IPv4 address, example: `random.domain.tld` returns a random IPv4 address
 - `<subdomain>.as.<ip>` - creates record to resolve subdomain name to the IPv4 address, example: `testname.as.1-1-1-1.domain.tld` resolves to `1.1.1.1`
 - `<subdomain>.lookup` - returns created on the previous step IPv4 record for the subdomain, example: `testname.lookup.domain.tld` resolves to `1.1.1.1`

See tests for more details.

## Install
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Run in Docker
Run:
```
make up
```
Check container status:
```
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                    PORTS                   NAMES
e353becd50f4   dnstrike:0.1.0   "python3 resolver.py…"   23 seconds ago   Up 22 seconds (healthy)   0.0.0.0:53->55053/udp   dnstrike
```
Test:
```bash
dig @127.0.0.1 1-2-3-4.bind.localhost
```
Expected output:
```
;; QUESTION SECTION:
;1-2-3-4.bind.localhost.                IN      A

;; ANSWER SECTION:
1-2-3-4.bind.localhost. 60      IN      A       1.2.3.4

;; Query time: 3 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sun Aug 07 00:47:58 +03 2022
;; MSG SIZE  rcvd: 56
```

## Self-Host
Requirements: domain name, VPS or any available machine.  

Create NS records so they will point to the resolver, example configuration:
```
Type: A, Name: ns1, Data: <machine (VPS) IP>
Type: A, Name: ns2, Data: <machine (VPS) IP>
Type: NS, Name: anything you want, Data: ns1.<domain.tld>
Type: NS, Name: anything you want, Data: ns2.<domain.tld>
```

## Tests
```bash
make test
```
Expected output:
```
Ran 7 tests in 0.007s

OK
```

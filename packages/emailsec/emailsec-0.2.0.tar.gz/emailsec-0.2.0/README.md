# emailsec

[![builds.sr.ht status](https://builds.sr.ht/~tsileo/emailsec.svg)](https://builds.sr.ht/~tsileo/emailsec?)

`emailsec` is a Python library that provides tools to parse and verify SPF (Sender Policy Framework) and DKIM (DomainKeys Identified Mail) records.

**This project is still in early development.**

## Sender Policy Framework

[RFC 7208](https://datatracker.ietf.org/doc/html/rfc7208)-compliant parser and checker.

### Parser

```
>>> from emailsec.spf.parser import parse_record
>>> parse_record("v=spf1 +a mx/30 mx:example.org/30 -all")
[A(qualifier=<Qualifier.PASS: '+'>, domain_spec=None, cidr=None),
 MX(qualifier=<Qualifier.PASS: '+'>, domain_spec=None, cidr='/30'),
 MX(qualifier=<Qualifier.PASS: '+'>, domain_spec='example.org', cidr='/30'),
 All(qualifier=<Qualifier.FAIL: '-'>)]
```

### Checker

```
>>> import asyncio
>>> from emailsec.spf.checker import check_host
>>>  asyncio.run(check_host(ip="192.0.2.10", sender="hello@example.com"))
(<Result.PASS: 'pass'>, '')
```

## Contribution

Contributions are welcome but please open an issue to start a discussion before starting something consequent.

## License

Copyright (c) 2025 Thomas Sileo and contributors. Released under the MIT license.

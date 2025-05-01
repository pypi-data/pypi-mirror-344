import unittest
import typing

from zone import Zone


class Test(unittest.TestCase):
    def test(self):
        SEP = "\n"

        lines_actual: typing.List[str] = [
            line.strip() for line in Zone(self.ZONE_JSON).csv().split(SEP)
        ]

        lines_expected: typing.List[str] = [
            line.strip() for line in self.CSV_EXPECTED.split(SEP)
        ]

        self.assertEqual(
            set(lines_actual),
            set(lines_expected),
        )

        return

    ZONE_JSON = r"""{
  "account": "",
  "api_rectify": false,
  "catalog": "",
  "dnssec": false,
  "edited_serial": 2025043001,
  "id": "export.example.com.",
  "kind": "Native",
  "last_check": 0,
  "master_tsig_key_ids": [],
  "masters": [],
  "name": "export.example.com.",
  "notified_serial": 0,
  "nsec3narrow": false,
  "nsec3param": "",
  "rrsets": [
    {
      "comments": [],
      "name": "usc-isic.export.example.com.",
      "records": [
        {
          "content": "C.ISI.EDU.",
          "disabled": false
        }
      ],
      "ttl": 86400,
      "type": "CNAME"
    },
    {
      "comments": [],
      "name": "vaxa.export.example.com.",
      "records": [
        {
          "content": "10.2.0.27",
          "disabled": false
        },
        {
          "content": "128.9.0.33",
          "disabled": false
        }
      ],
      "ttl": 300,
      "type": "A"
    },
    {
      "comments": [],
      "name": "venera.export.example.com.",
      "records": [
        {
          "content": "10.1.0.52",
          "disabled": true
        },
        {
          "content": "128.9.0.32",
          "disabled": false
        }
      ],
      "ttl": 300,
      "type": "A"
    },
    {
      "comments": [],
      "name": "export.example.com.",
      "records": [
        {
          "content": "\"v=DMARC1;p=none;sp=quarantine;pct=100;rua=mailto:dmarcreports@example.com;\"",
          "disabled": false
        }
      ],
      "ttl": 14400,
      "type": "TXT"
    },
    {
      "comments": [],
      "name": "export.example.com.",
      "records": [
        {
          "content": "10 VAXA.ISI.EDU.",
          "disabled": false
        },
        {
          "content": "10 VENERA.ISI.EDU.",
          "disabled": false
        }
      ],
      "ttl": 3600,
      "type": "MX"
    },
    {
      "comments": [],
      "name": "export.example.com.",
      "records": [
        {
          "content": "a.misconfigured.dns.server.invalid. hostmaster.export.example.com. 2025043001 10800 3600 604800 3600",
          "disabled": false
        }
      ],
      "ttl": 3600,
      "type": "SOA"
    },
    {
      "comments": [],
      "name": "export.example.com.",
      "records": [
        {
          "content": "ns0.example.com.",
          "disabled": false
        }
      ],
      "ttl": 3600,
      "type": "NS"
    }
  ],
  "serial": 2025043001,
  "slave_tsig_key_ids": [],
  "soa_edit": "",
  "soa_edit_api": "DEFAULT",
  "url": "/api/v1/servers/localhost/zones/export.example.com."
}"""

    CSV_EXPECTED = r'''export.example.com.,3600,IN,MX,10 VAXA.ISI.EDU.
export.example.com.,3600,IN,MX,10 VENERA.ISI.EDU.
export.example.com.,3600,IN,NS,ns0.example.com.
export.example.com.,3600,IN,SOA,a.misconfigured.dns.server.invalid. hostmaster.export.example.com. 2025043001 10800 3600 604800 3600
export.example.com.,14400,IN,TXT,"""v=DMARC1;p=none;sp=quarantine;pct=100;rua=mailto:dmarcreports@example.com;"""
usc-isic.export.example.com.,86400,IN,CNAME,C.ISI.EDU.
vaxa.export.example.com.,300,IN,A,10.2.0.27
vaxa.export.example.com.,300,IN,A,128.9.0.33
venera.export.example.com.,300,IN,A,128.9.0.32'''

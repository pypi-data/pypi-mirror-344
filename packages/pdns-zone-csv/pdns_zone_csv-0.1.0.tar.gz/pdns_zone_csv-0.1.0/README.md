```pycon
>>> from pdns_zone_csv import Zone
>>> # https://doc.powerdns.com/authoritative/http-api/zone.html#listing-a-zone
>>> zone_json = r'{"account": "", "api_rectify": false, "dnssec": false, "edited_serial": 2022040501, "id": "example.org.", "kind": "Native", "last_check": 0, "master_tsig_key_ids": [], "masters": [], "name": "example.org.", "notified_serial": 0, "nsec3narrow": false, "nsec3param": "", "rrsets": [{"comments": [], "name": "example.org.", "records": [{"content": "a.misconfigured.dns.server.invalid. hostmaster.example.org. 2022040501 10800 3600 604800 3600", "disabled": false}], "ttl": 3600, "type": "SOA"}, {"comments": [], "name": "example.org.", "records": [{"content": "ns1.example.org.", "disabled": false}, {"content": "ns2.example.org.", "disabled": false}], "ttl": 3600, "type": "NS"}], "serial": 2022040501, "slave_tsig_key_ids": [], "soa_edit": "", "soa_edit_api": "DEFAULT", "url": "/api/v1/servers/localhost/zones/example.org."}'
>>> zone_csv = Zone(zone_json).csv()
>>> print(zone_csv)
example.org.,3600,IN,SOA,a.misconfigured.dns.server.invalid. hostmaster.example.org. 2022040501 10800 3600 604800 3600
example.org.,3600,IN,NS,ns1.example.org.
example.org.,3600,IN,NS,ns2.example.org.
```

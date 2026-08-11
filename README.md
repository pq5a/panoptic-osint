# PANOPTIC

A CLI with 27 OSINT lookups in it. WHOIS, DNS, subdomain enum, IP/ASN info,
TLS cert dump, username checks across a bunch of sites, some file/hash/encoding
utilities, etc. One command, JSON out, pipe it into whatever you want.

Everything in here only touches public data - RDAP, crt.sh, plain DNS, public
HTTP endpoints. No exploits, no login bypass, no scraping stuff that isn't
already public. If you're doing recon on something you own or have permission
to test, this should cover a decent chunk of the boring parts.

## install

```bash
git clone https://github.com/pq5a/panoptic-osint.git
cd panoptic-osint
pip install -r requirements.txt
pip install -e .
```

## usage

```
panoptic modules          # see everything it can do
panoptic whois example.com
panoptic dns example.com
panoptic subdomains example.com
panoptic geoip 1.1.1.1
panoptic username someuser
panoptic sslinfo github.com
panoptic hashid 5f4dcc3b5aa765d61d8327deb882cf99
```

running `panoptic modules` prints something like this:

```
PANOPTIC
--------
27 modules

[1] whois <domain> - whois / rdap lookup
[2] dns <domain> - a/aaaa/mx/ns/txt/cname/soa records
[3] rdns <ip> - reverse dns (ptr) lookup
...
```

every command just prints json, so `panoptic dns example.com | jq .A` works fine.

## what's in it

network / domain stuff:
- whois - rdap-based, no local whois binary needed
- dns - all the common record types in one shot
- rdns - reverse lookup
- subdomains - pulls subdomains out of certificate transparency logs (crt.sh)
- geoip / asn - where is this ip, who owns it
- portscan - plain tcp connect scan on common ports, nothing fancy
- headers - dump response headers
- sslinfo - cert subject/issuer/expiry
- dnssec - is it turned on
- mailsec - spf/dmarc presence
- robots - robots.txt + sitemap.xml
- wayback - has this url been archived
- techstack - rough guess at what a site is built with, from headers/html hints

identity stuff:
- username - checks 15 platforms for a given handle
- ghuser - github's public api, basically
- gravatar - does this email have a gravatar
- emailcheck - syntax + mx record sanity check, not a deliverability test
- phone - country/carrier/type via libphonenumber's data

misc:
- exif - pull metadata out of an image file
- reverseimg - builds reverse image search urls (doesn't hit them itself)
- dorks - generates google dork strings for a domain
- leaklinks - links to HIBP/DeHashed/IntelX for a query, doesn't query them for you
- unshorten - follows a shortened url
- hashid - guesses what kind of hash a string is, based on length/pattern
- b64decode - exactly what it says
- logo - clearbit's free logo endpoint

## a note on scope

Don't point `portscan` or anything else at systems you don't own or don't have
permission to test. Nothing in this repo does anything illegal on its own, but
how you use it is on you.

## license

MIT, see LICENSE.

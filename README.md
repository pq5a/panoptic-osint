```
 ██▓███   ▄▄▄       ███▄    █  ▒█████   ██▓███  ▄▄▄█████▓ ██▓ ▄████▄
▓██░  ██▒▒████▄     ██ ▀█   █ ▒██▒  ██▒▓██░  ██▒▓  ██▒ ▓▒▓██▒▒██▀ ▀█
▓██░ ██▓▒▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██░ ██▓▒▒ ▓██░ ▒░▒██▒▒▓█    ▄
▒██▄█▓▒ ▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒██▄█▓▒ ▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒
▒██▒ ░  ░ ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░▒██▒ ░  ░  ▒██▒ ░ ░██░▒ ▓███▀ ░
▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ▒▓▒░ ░  ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░
░▒ ░       ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░▒ ░         ░     ▒ ░  ░  ▒
░░         ░   ▒      ░   ░ ░ ░ ░ ░ ▒  ░░         ░       ▒ ░░
               ░  ░         ░     ░ ░                     ░  ░ ░
                                                               ░
        O S I N T   R E C O N N A I S S A N C E   F R A M E W O R K
```

<p align="center">
  <b>27 modules · zero API keys required to start · one target, total visibility</b><br>
  <sub>Domain & network recon · identity & social footprint · file/metadata & utility tooling</sub>
</p>

<p align="center">
  <img alt="python" src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="modules" src="https://img.shields.io/badge/modules-27-orange">
</p>

---

## What is PANOPTIC?

**PANOPTIC** is a single-CLI OSINT reconnaissance framework that aggregates 27
open-source-intelligence lookups — DNS, WHOIS/RDAP, certificate-transparency
subdomain discovery, IP/ASN geolocation, TLS inspection, cross-platform
username enumeration, public-metadata phone/email checks, EXIF extraction,
hash identification, and more — behind one consistent command.

It's built for security researchers, red teamers (with authorization),
journalists, and anyone doing legitimate footprint analysis on domains,
infrastructure, or their own public digital presence.

Every module works against **public, unauthenticated data sources only**
(RDAP registries, crt.sh, public DNS, public HTTP endpoints, public APIs).
Nothing here breaks into systems, bypasses authentication, or scrapes
private/gated data.

## Install

```bash
git clone https://github.com/pq5a/panoptic-osint.git
cd panoptic-osint
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
panoptic modules                     # list all 27 modules
panoptic whois example.com
panoptic dns example.com
panoptic subdomains example.com
panoptic geoip 1.1.1.1
panoptic username johndoe
panoptic ghuser torvalds
panoptic sslinfo github.com
panoptic hashid 5f4dcc3b5aa765d61d8327deb882cf99
panoptic dorks example.com
```

Every command prints structured JSON, so PANOPTIC pipes cleanly into `jq`,
other tooling, or your own scripts.

## Module catalogue (27)

### Network & domain (14)
| Command | Description |
|---|---|
| `whois` | WHOIS / RDAP registration lookup |
| `dns` | A / AAAA / MX / NS / TXT / CNAME / SOA records |
| `rdns` | Reverse DNS (PTR) lookup |
| `subdomains` | Passive subdomain enumeration via crt.sh certificate transparency |
| `geoip` | IP / host geolocation |
| `asn` | ASN & network ownership lookup |
| `portscan` | TCP connect scan of common ports (authorized targets only) |
| `headers` | HTTP response headers |
| `sslinfo` | TLS certificate details |
| `dnssec` | DNSSEC enablement check |
| `mailsec` | SPF / DMARC record check |
| `robots` | robots.txt & sitemap.xml fetch |
| `wayback` | Wayback Machine snapshot lookup |
| `techstack` | Lightweight tech-stack fingerprint |

### Identity & social footprint (5)
| Command | Description |
|---|---|
| `username` | Cross-platform username presence check (15 sites) |
| `ghuser` | GitHub public profile info |
| `gravatar` | Gravatar avatar/profile lookup |
| `emailcheck` | Email syntax + MX sanity check |
| `phone` | Phone number country/carrier/type lookup (public metadata) |

### Files & utility (8)
| Command | Description |
|---|---|
| `exif` | Extract EXIF metadata from an image file |
| `reverseimg` | Reverse image search link generator (Google/Yandex/TinEye/Bing) |
| `dorks` | Google dork generator for a domain |
| `leaklinks` | Public breach/leak lookup service links (HIBP, DeHashed, IntelX) |
| `unshorten` | Expand a shortened URL |
| `hashid` | Identify a hash's likely algorithm |
| `b64decode` | Decode a base64 string |
| `logo` | Company logo lookup by domain |

## Ethics & scope

PANOPTIC is a **passive/public-data** framework. Use it only on:
- Domains, systems, and accounts you own, or
- Targets you have explicit written authorization to assess.

`portscan` opens plain TCP connections to check port availability — treat it
the same as any authorized recon activity and follow local law and the
target's policies. This project does not, and will not, include exploit
code, credential-bruteforcing, private-data scraping, or anything designed
to bypass authentication.

## Contributing

PRs welcome — new modules should stick to public/passive data sources and
include a short docstring explaining what they check and why it's safe.

## License

MIT — see [LICENSE](LICENSE).

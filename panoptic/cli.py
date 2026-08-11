"""PANOPTIC CLI — 27 OSINT modules, one entrypoint."""
import argparse
import json
import sys

from panoptic.banner import print_banner
from panoptic.modules import network as net
from panoptic.modules import social as soc
from panoptic.modules import utils_osint as util


def _out(data):
    print(json.dumps(data, indent=2, default=str))


COMMANDS = {
    # --- network / domain (14) ---
    "whois": (net.whois_lookup, "domain", "WHOIS / RDAP registration lookup"),
    "dns": (net.dns_records, "domain", "A/AAAA/MX/NS/TXT/CNAME/SOA records"),
    "rdns": (net.reverse_dns, "ip", "Reverse DNS (PTR) lookup"),
    "subdomains": (net.subdomain_enum, "domain", "Passive subdomain enum via crt.sh"),
    "geoip": (net.geoip_lookup, "target", "IP / host geolocation"),
    "asn": (net.asn_lookup, "ip", "ASN & network ownership lookup"),
    "portscan": (net.port_scan, "host", "TCP connect scan of common ports"),
    "headers": (net.http_headers, "url", "HTTP response headers"),
    "sslinfo": (net.ssl_certificate_info, "host", "TLS certificate details"),
    "dnssec": (net.dnssec_check, "domain", "DNSSEC enablement check"),
    "mailsec": (net.email_security_records, "domain", "SPF / DMARC record check"),
    "robots": (net.robots_and_sitemap, "url", "robots.txt & sitemap.xml fetch"),
    "wayback": (net.wayback_snapshots, "url", "Wayback Machine snapshot lookup"),
    "techstack": (net.tech_fingerprint, "url", "Lightweight tech-stack fingerprint"),
    # --- identity / social (5) ---
    "username": (soc.username_search, "username", "Cross-platform username search (15 sites)"),
    "ghuser": (soc.github_user_info, "username", "GitHub public profile info"),
    "gravatar": (soc.gravatar_lookup, "email", "Gravatar avatar/profile lookup"),
    "emailcheck": (soc.email_format_check, "email", "Email syntax + MX sanity check"),
    "phone": (soc.phone_number_info, "number", "Phone number country/carrier/type lookup"),
    # --- utility (8) ---
    "exif": (util.exif_metadata, "image_path", "Extract EXIF metadata from an image file"),
    "reverseimg": (util.reverse_image_search_links, "image_url", "Reverse image search link generator"),
    "dorks": (util.google_dork_generator, "domain", "Google dork generator for a domain"),
    "leaklinks": (util.leak_search_links, "query", "Public breach/leak lookup service links"),
    "unshorten": (util.url_expander, "short_url", "Expand a shortened URL"),
    "hashid": (util.hash_identifier, "value", "Identify a hash's likely algorithm"),
    "b64decode": (util.base64_decode, "value", "Decode a base64 string"),
    "logo": (util.company_logo_lookup, "domain", "Company logo lookup by domain"),
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="panoptic",
        description="PANOPTIC — an OSINT reconnaissance framework with 27 modules.",
    )
    parser.add_argument("--no-banner", action="store_true", help="Suppress the startup banner")
    sub = parser.add_subparsers(dest="command", required=True)

    for name, (_, argname, help_text) in COMMANDS.items():
        p = sub.add_parser(name, help=help_text)
        p.add_argument(argname)

    list_p = sub.add_parser("modules", help="List all available modules")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.no_banner and args.command != "modules":
        print_banner()

    if args.command == "modules":
        print_banner()
        print(f"{len(COMMANDS)} modules available:\n")
        for name, (_, argname, help_text) in COMMANDS.items():
            print(f"  panoptic {name:<12} <{argname:<12}>  — {help_text}")
        return

    func, argname, _ = COMMANDS[args.command]
    value = getattr(args, argname)
    result = func(value)
    _out(result)


if __name__ == "__main__":
    sys.exit(main())

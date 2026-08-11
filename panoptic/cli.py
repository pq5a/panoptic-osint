# entrypoint. wires the modules up to argparse and dumps json to stdout.
import argparse
import json
import sys

from panoptic.banner import print_banner, print_module_list
from panoptic.modules import network as net
from panoptic.modules import social as soc
from panoptic.modules import utils_osint as util


def _out(data):
    print(json.dumps(data, indent=2, default=str))


# name -> (function, cli arg name, short description)
COMMANDS = {
    "whois": (net.whois_lookup, "domain", "whois / rdap lookup"),
    "dns": (net.dns_records, "domain", "a/aaaa/mx/ns/txt/cname/soa records"),
    "rdns": (net.reverse_dns, "ip", "reverse dns (ptr) lookup"),
    "subdomains": (net.subdomain_enum, "domain", "subdomain enum via crt.sh"),
    "geoip": (net.geoip_lookup, "target", "ip/host geolocation"),
    "asn": (net.asn_lookup, "ip", "asn + network owner lookup"),
    "portscan": (net.port_scan, "host", "tcp connect scan, common ports only"),
    "headers": (net.http_headers, "url", "http response headers"),
    "sslinfo": (net.ssl_certificate_info, "host", "tls cert details"),
    "dnssec": (net.dnssec_check, "domain", "dnssec on/off"),
    "mailsec": (net.email_security_records, "domain", "spf/dmarc check"),
    "robots": (net.robots_and_sitemap, "url", "robots.txt + sitemap.xml"),
    "wayback": (net.wayback_snapshots, "url", "wayback machine snapshots"),
    "techstack": (net.tech_fingerprint, "url", "rough tech stack guess"),
    "username": (soc.username_search, "username", "check a username across 15 sites"),
    "ghuser": (soc.github_user_info, "username", "github profile info"),
    "gravatar": (soc.gravatar_lookup, "email", "gravatar lookup"),
    "emailcheck": (soc.email_format_check, "email", "syntax + mx check"),
    "phone": (soc.phone_number_info, "number", "country/carrier/type lookup"),
    "exif": (util.exif_metadata, "image_path", "pull exif data from an image"),
    "reverseimg": (util.reverse_image_search_links, "image_url", "reverse image search links"),
    "dorks": (util.google_dork_generator, "domain", "google dork list for a domain"),
    "leaklinks": (util.leak_search_links, "query", "links to public breach lookup sites"),
    "unshorten": (util.url_expander, "short_url", "follow a shortened url"),
    "hashid": (util.hash_identifier, "value", "guess the hash algo"),
    "b64decode": (util.base64_decode, "value", "decode base64"),
    "logo": (util.company_logo_lookup, "domain", "company logo by domain"),
}


def build_parser():
    parser = argparse.ArgumentParser(prog="panoptic")
    parser.add_argument("--no-banner", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    for name, (_, argname, help_text) in COMMANDS.items():
        p = sub.add_parser(name, help=help_text)
        p.add_argument(argname)

    sub.add_parser("modules", help="list everything this thing can do")
    return parser


def main():
    args = build_parser().parse_args()

    if not args.no_banner:
        print_banner()

    if args.command == "modules":
        print_module_list(COMMANDS)
        return

    func, argname, _ = COMMANDS[args.command]
    result = func(getattr(args, argname))
    _out(result)


if __name__ == "__main__":
    sys.exit(main())

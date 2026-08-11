"""Network & domain reconnaissance modules (DNS, WHOIS, IP, certs, etc.)."""
import socket
import ssl
import datetime
import requests

TIMEOUT = 8


def whois_lookup(domain: str) -> dict:
    """RDAP-based WHOIS lookup (no local whois binary required)."""
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=TIMEOUT)
        if r.status_code != 200:
            return {"error": f"RDAP lookup failed ({r.status_code})"}
        data = r.json()
        events = {e.get("eventAction"): e.get("eventDate") for e in data.get("events", [])}
        return {
            "domain": data.get("ldhName", domain),
            "status": data.get("status", []),
            "registered": events.get("registration"),
            "last_changed": events.get("last changed"),
            "expires": events.get("expiration"),
            "nameservers": [ns.get("ldhName") for ns in data.get("nameservers", [])],
        }
    except Exception as e:
        return {"error": str(e)}


def dns_records(domain: str) -> dict:
    """Resolve common DNS record types via dnspython."""
    import dns.resolver

    results = {}
    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=TIMEOUT)
            results[rtype] = [r.to_text() for r in answers]
        except Exception:
            results[rtype] = []
    return results


def reverse_dns(ip: str) -> dict:
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return {"ip": ip, "hostname": host}
    except Exception as e:
        return {"ip": ip, "error": str(e)}


def subdomain_enum(domain: str) -> dict:
    """Passive subdomain enumeration via certificate-transparency logs (crt.sh)."""
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=15)
        if r.status_code != 200:
            return {"error": f"crt.sh returned {r.status_code}"}
        names = set()
        for entry in r.json():
            for n in entry.get("name_value", "").split("\n"):
                n = n.strip().lstrip("*.")
                if n and domain in n:
                    names.add(n)
        return {"count": len(names), "subdomains": sorted(names)}
    except Exception as e:
        return {"error": str(e)}


def geoip_lookup(ip_or_host: str) -> dict:
    try:
        r = requests.get(f"http://ip-api.com/json/{ip_or_host}", timeout=TIMEOUT)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def asn_lookup(ip: str) -> dict:
    """ASN / network ownership info."""
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=TIMEOUT)
        data = r.json()
        return {
            "ip": ip,
            "asn": data.get("asn"),
            "org": data.get("org"),
            "network": data.get("network"),
            "country": data.get("country_name"),
        }
    except Exception as e:
        return {"error": str(e)}


def port_scan(host: str, ports=None) -> dict:
    """Lightweight TCP connect scan of common ports. Intended for hosts you own or are authorized to test."""
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 8080, 8443]
    open_ports = []
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        return {"error": str(e)}
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
        finally:
            s.close()
    return {"host": host, "ip": ip, "open_ports": open_ports}


def http_headers(url: str) -> dict:
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        return {"url": r.url, "status": r.status_code, "headers": dict(r.headers)}
    except Exception as e:
        return {"error": str(e)}


def ssl_certificate_info(host: str, port: int = 443) -> dict:
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        return {
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "not_before": cert.get("notBefore"),
            "not_after": cert.get("notAfter"),
            "san": [v for k, v in cert.get("subjectAltName", [])],
        }
    except Exception as e:
        return {"error": str(e)}


def dnssec_check(domain: str) -> dict:
    import dns.resolver

    try:
        answers = dns.resolver.resolve(domain, "DNSKEY", lifetime=TIMEOUT)
        return {"domain": domain, "dnssec_enabled": True, "keys": len(answers)}
    except Exception:
        return {"domain": domain, "dnssec_enabled": False}


def email_security_records(domain: str) -> dict:
    """Check SPF / DMARC / DKIM presence for a domain."""
    import dns.resolver

    out = {"spf": None, "dmarc": None}
    try:
        txts = dns.resolver.resolve(domain, "TXT", lifetime=TIMEOUT)
        for t in txts:
            text = t.to_text().strip('"')
            if text.startswith("v=spf1"):
                out["spf"] = text
    except Exception:
        pass
    try:
        dmarc = dns.resolver.resolve(f"_dmarc.{domain}", "TXT", lifetime=TIMEOUT)
        out["dmarc"] = dmarc[0].to_text().strip('"')
    except Exception:
        pass
    return out


def robots_and_sitemap(url: str) -> dict:
    if not url.startswith("http"):
        url = "https://" + url
    result = {}
    for path in ["robots.txt", "sitemap.xml"]:
        try:
            r = requests.get(url.rstrip("/") + "/" + path, timeout=TIMEOUT)
            result[path] = r.text[:2000] if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception as e:
            result[path] = str(e)
    return result


def wayback_snapshots(url: str) -> dict:
    try:
        r = requests.get(
            "http://archive.org/wayback/available", params={"url": url}, timeout=TIMEOUT
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def tech_fingerprint(url: str) -> dict:
    """Very lightweight tech-stack fingerprint from headers + HTML hints."""
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=TIMEOUT)
        headers = r.headers
        html = r.text.lower()
        checks = {
            "WordPress": "wp-content" in html,
            "Shopify": "cdn.shopify.com" in html,
            "React": "react" in html or "__next" in html,
            "Cloudflare": "cloudflare" in headers.get("Server", "").lower()
            or "cf-ray" in headers,
            "Nginx": "nginx" in headers.get("Server", "").lower(),
            "Apache": "apache" in headers.get("Server", "").lower(),
            "PHP": "x-powered-by" in headers and "php" in headers.get("X-Powered-By", "").lower(),
        }
        hints = [name for name, matched in checks.items() if matched]
        return {"url": r.url, "server": headers.get("Server"), "detected": hints}
    except Exception as e:
        return {"error": str(e)}

"""Utility recon modules: metadata, encodings, dork/link generators."""
import base64
import binascii
import re
import requests

TIMEOUT = 8


def exif_metadata(image_path: str) -> dict:
    try:
        import exifread

        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, details=False)
        if not tags:
            return {"image": image_path, "exif_found": False}
        return {
            "image": image_path,
            "exif_found": True,
            "tags": {k: str(v) for k, v in tags.items()},
        }
    except Exception as e:
        return {"error": str(e)}


def reverse_image_search_links(image_url: str) -> dict:
    """Generate reverse-image-search URLs (Google, Yandex, TinEye, Bing)."""
    return {
        "google": f"https://lens.google.com/uploadbyurl?url={image_url}",
        "yandex": f"https://yandex.com/images/search?rpt=imageview&url={image_url}",
        "tineye": f"https://tineye.com/search?url={image_url}",
        "bing": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{image_url}",
    }


def google_dork_generator(domain: str) -> dict:
    """Generate common Google-dork search strings for a domain (for use in a search engine, not automated scraping)."""
    dorks = [
        f'site:{domain} filetype:pdf',
        f'site:{domain} filetype:xls OR filetype:xlsx',
        f'site:{domain} inurl:admin',
        f'site:{domain} inurl:login',
        f'site:{domain} intitle:"index of"',
        f'site:{domain} ext:log',
        f'site:{domain} "confidential"',
        f'site:pastebin.com "{domain}"',
        f'site:linkedin.com "{domain}"',
    ]
    return {"domain": domain, "dorks": dorks}


def leak_search_links(query: str) -> dict:
    """Generate links to legitimate public breach/leak lookup services (does not query any data itself)."""
    return {
        "haveibeenpwned": f"https://haveibeenpwned.com/account/{query}",
        "dehashed": f"https://dehashed.com/search?query={query}",
        "intelx": f"https://intelx.io/?s={query}",
    }


def url_expander(short_url: str) -> dict:
    try:
        r = requests.head(short_url, allow_redirects=True, timeout=TIMEOUT)
        return {"original": short_url, "resolved": r.url, "status": r.status_code}
    except Exception as e:
        return {"error": str(e)}


HASH_PATTERNS = [
    (r"^[a-f0-9]{32}$", "MD5"),
    (r"^[a-f0-9]{40}$", "SHA-1"),
    (r"^[a-f0-9]{64}$", "SHA-256"),
    (r"^[a-f0-9]{96}$", "SHA-384"),
    (r"^[a-f0-9]{128}$", "SHA-512"),
    (r"^\$2[aby]\$.{56}$", "bcrypt"),
    (r"^\$1\$.+\$.+$", "MD5-crypt"),
    (r"^[a-f0-9]{32}:[a-zA-Z0-9]+$", "Salted MD5"),
]


def hash_identifier(value: str) -> dict:
    value = value.strip()
    matches = [name for pattern, name in HASH_PATTERNS if re.match(pattern, value, re.IGNORECASE)]
    return {"value": value, "possible_types": matches or ["Unknown"]}


def base64_decode(value: str) -> dict:
    try:
        decoded = base64.b64decode(value).decode("utf-8", errors="replace")
        return {"input": value, "decoded": decoded}
    except (binascii.Error, ValueError) as e:
        return {"error": str(e)}


def company_logo_lookup(domain: str) -> dict:
    """Public company logo/branding lookup via Clearbit's free logo API."""
    return {"domain": domain, "logo_url": f"https://logo.clearbit.com/{domain}"}

# username / email / phone stuff. all public pages, nothing that needs a login.
import hashlib
import requests

TIMEOUT = 6

# just checking if a profile url returns 200. not scraping anything private,
# and some of these (reddit, x) are flaky about status codes so treat this
# as "probably exists" not gospel.
USERNAME_SITES = {
    "GitHub": "https://github.com/{u}",
    "GitLab": "https://gitlab.com/{u}",
    "Reddit": "https://www.reddit.com/user/{u}/about.json",
    "X (Twitter)": "https://x.com/{u}",
    "Instagram": "https://www.instagram.com/{u}/",
    "TikTok": "https://www.tiktok.com/@{u}",
    "YouTube": "https://www.youtube.com/@{u}",
    "Twitch": "https://www.twitch.tv/{u}",
    "Medium": "https://medium.com/@{u}",
    "DEV.to": "https://dev.to/{u}",
    "HackerNews": "https://news.ycombinator.com/user?id={u}",
    "Pinterest": "https://www.pinterest.com/{u}/",
    "Steam": "https://steamcommunity.com/id/{u}",
    "Keybase": "https://keybase.io/{u}",
    "Docker Hub": "https://hub.docker.com/u/{u}",
}


def username_search(username):
    found, not_found, errors = [], [], []
    headers = {"User-Agent": "Mozilla/5.0 (PANOPTIC)"}
    for site, template in USERNAME_SITES.items():
        url = template.format(u=username)
        try:
            r = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
            if r.status_code == 200:
                found.append({"site": site, "url": url})
            else:
                not_found.append(site)
        except Exception:
            errors.append(site)
    return {"username": username, "found": found, "not_found": not_found, "errors": errors}


def github_user_info(username):
    try:
        r = requests.get(f"https://api.github.com/users/{username}", timeout=TIMEOUT)
        if r.status_code != 200:
            return {"error": f"github api returned {r.status_code}"}
        d = r.json()
        return {
            "login": d.get("login"),
            "name": d.get("name"),
            "bio": d.get("bio"),
            "company": d.get("company"),
            "location": d.get("location"),
            "blog": d.get("blog"),
            "public_repos": d.get("public_repos"),
            "followers": d.get("followers"),
            "created_at": d.get("created_at"),
        }
    except Exception as e:
        return {"error": str(e)}


def gravatar_lookup(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        return {
            "email_hash": email_hash,
            "avatar_exists": r.status_code == 200,
            "profile_url": f"https://www.gravatar.com/{email_hash}",
        }
    except Exception as e:
        return {"error": str(e)}


def email_format_check(email):
    # just a sanity check, not a deliverability guarantee
    import re
    import dns.resolver

    valid_syntax = bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))
    result = {"email": email, "valid_syntax": valid_syntax, "domain_has_mx": False}
    if valid_syntax:
        domain = email.split("@")[1]
        try:
            mx = dns.resolver.resolve(domain, "MX", lifetime=TIMEOUT)
            result["domain_has_mx"] = len(mx) > 0
        except Exception:
            result["domain_has_mx"] = False
    return result


def phone_number_info(number):
    # libphonenumber's data, not some external lookup service
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, number_type

        parsed = phonenumbers.parse(number, None)
        return {
            "number": number,
            "valid": phonenumbers.is_valid_number(parsed),
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en") or "unknown",
            "type": str(number_type(parsed)),
            "international_format": phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),
        }
    except Exception as e:
        return {"error": str(e)}

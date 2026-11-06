"""Rule-based phishing-URL heuristic checker.

Scores a URL against a set of weighted lexical/host heuristics. This is NOT a
machine-learning classifier and not a safe-browsing lookup — it only flags
structural patterns commonly seen in phishing links. Treat the score as a hint,
not a verdict.
"""

from __future__ import annotations

import argparse
import ipaddress
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

SHORTENERS = ("bit.ly", "t.co", "tinyurl.com", "goo.gl", "ow.ly", "buff.ly", "is.gd", "tiny.cc")

WEIGHTS = {
    "ip_in_host": 30,
    "at_symbol": 25,
    "shortener": 20,
    "punycode": 20,
    "long_url": 10,
    "many_dashes": 10,
    "multiple_double_slash": 10,
    "no_https": 5,
}


@dataclass
class Report:
    url: str
    host: str
    score: int
    verdict: str
    flags: list[str] = field(default_factory=list)


def normalize(url: str) -> tuple[str, str]:
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    parsed = urlparse(url)
    host = parsed.netloc.split("@")[-1].split(":")[0].lower()
    return url, host


def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def analyze(url: str) -> Report:
    url, host = normalize(url)
    parsed = urlparse(url)
    flags: list[str] = []
    score = 0

    def add(cond: bool, key: str, msg: str) -> None:
        nonlocal score
        if cond:
            flags.append(msg)
            score += WEIGHTS[key]

    add(is_ip(host), "ip_in_host", "Raw IP address used as host")
    add("@" in parsed.netloc, "at_symbol", "'@' in authority (can hide the real host)")
    add(host in SHORTENERS, "shortener", "Known URL shortener")
    add(host.startswith("xn--") or ".xn--" in host, "punycode", "Punycode host (possible homograph)")
    add(len(url) > 75, "long_url", "Unusually long URL")
    add(host.count("-") > 4, "many_dashes", "Many hyphens in host")
    add(url.count("//") > 1, "multiple_double_slash", "Extra '//' in path")
    add(parsed.scheme != "https", "no_https", "Not HTTPS")

    verdict = "High Risk" if score >= 50 else "Medium Risk" if score >= 20 else "Low Risk"
    return Report(url=url, host=host, score=score, verdict=verdict, flags=flags)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Rule-based phishing-URL heuristic checker")
    ap.add_argument("url", nargs="?", help="URL to analyze (prompted if omitted)")
    args = ap.parse_args(argv)
    url = args.url or input("Enter URL: ")

    r = analyze(url)
    print(f"\nURL:     {r.url}")
    print(f"Host:    {r.host}")
    print(f"Score:   {r.score}")
    print(f"Verdict: {r.verdict}")
    if r.flags:
        print("Flags:")
        for f in r.flags:
            print(f"  - {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

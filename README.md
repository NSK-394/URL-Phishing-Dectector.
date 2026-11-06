# URL Phishing Checker

![tests](https://github.com/NSK-394/URL-Phishing-Dectector./actions/workflows/tests.yml/badge.svg)

A lightweight, **rule-based** heuristic checker for suspicious URLs. It scores a URL against weighted lexical and host-based signals that often appear in phishing links, and returns a Low / Medium / High risk verdict with the reasons.

> This is a **heuristic hint, not a verdict.** It is not a machine-learning model and not a safe-browsing/reputation lookup. A clean score does not mean a URL is safe, and a high score does not prove it's malicious.

## Signals checked
| Signal | Weight | Why it's suspicious |
|---|---|---|
| Raw IP as host | 30 | Legit sites use domain names |
| `@` in the authority | 25 | Everything before `@` is ignored by the browser — hides the real host |
| Known URL shortener | 20 | Obscures the destination |
| Punycode host (`xn--`) | 20 | Homograph attacks (`аpple.com` with a Cyrillic `а`) |
| Very long URL (>75) | 10 | Padding to bury the real domain |
| Many hyphens in host | 10 | `secure-paypal-login-account.com` |
| Extra `//` in path | 10 | Open-redirect / obfuscation |
| Not HTTPS | 5 | Weak signal on its own |

## Usage
```bash
python phishing_check.py "http://paypal.com@192.168.0.1/login"
```
```
URL:     http://paypal.com@192.168.0.1/login
Host:    192.168.0.1
Score:   55
Verdict: High Risk
Flags:
  - Raw IP address used as host
  - '@' in authority (can hide the real host)
```

## Limitations & next steps
- Purely lexical: it never fetches the URL, so it can't see redirects, page content, or TLS cert details
- Fixed weights, not learned — a labeled dataset + a simple classifier (logistic regression on these same features) would be the natural next version, and would justify calling it "ML"
- No allowlist, so a long legitimate URL can score Medium

## Tests
```bash
pip install pytest && pytest -q
```

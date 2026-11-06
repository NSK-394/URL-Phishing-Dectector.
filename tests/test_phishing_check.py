from phishing_check import analyze, normalize


def test_clean_https_url_is_low_risk():
    r = analyze("https://www.github.com/NSK-394")
    assert r.verdict == "Low Risk"
    assert r.score == 0


def test_ip_host_and_at_symbol_flagged():
    r = analyze("http://trusted.com@192.168.0.1/login")
    assert "Raw IP address used as host" in r.flags
    assert r.score >= 50
    assert r.verdict == "High Risk"


def test_punycode_flagged():
    assert any("Punycode" in f for f in analyze("http://xn--pple-43d.com").flags)


def test_normalize_strips_userinfo_and_port():
    _, host = normalize("https://user@evil.example.com:8443/x")
    assert host == "evil.example.com"

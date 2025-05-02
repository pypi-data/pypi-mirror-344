
from requestgo import get

def test_google():
    r = get("https://example.com")
    assert r.status_code == 200 or r.status_code == 301

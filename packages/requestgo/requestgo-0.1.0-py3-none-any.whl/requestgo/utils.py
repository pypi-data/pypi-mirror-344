
def parse_url(url):
    if url.startswith("https://"):
        return url[8:], 443, True
    elif url.startswith("http://"):
        return url[7:], 80, False
    else:
        raise ValueError("URL must start with http:// or https://")

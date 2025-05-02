
import socket
import ssl
import time
import random
from .response import Response
from .utils import parse_url

def _build_request(method, host, path, headers, body=None):
    request = f"{method} {path} HTTP/1.1\r\n"
    for k, v in headers.items():
        request += f"{k}: {v}\r\n"
    request += "\r\n"
    if body:
        request += body
    return request

def _send(host, port, data, use_ssl=True):
    with socket.create_connection((host, port)) as sock:
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        sock.sendall(data.encode())
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        return response.decode(errors='ignore')

def request(method, url, headers=None, data=None, anonymous=False, gentle=False):
    if gentle:
        time.sleep(random.uniform(0.5, 2.0))
    
    host_path, port, use_ssl = parse_url(url)
    host, *path = host_path.split("/")
    path = "/" + "/".join(path)
    
    if anonymous:
        headers = {
            "Host": host,
            "Accept": "*/*",
            "Connection": "close"
        }
    elif gentle:
        headers = {
            "Host": host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    else:
        headers = headers or {}
        headers.setdefault("User-Agent", "requestgo/fast")

    req = _build_request(method.upper(), host, path, headers, data)
    raw = _send(host, port, req, use_ssl)
    return Response(raw)

def get(url, headers=None, anonymous=False, gentle=False):
    return request("GET", url, headers=headers, anonymous=anonymous, gentle=gentle)

def post(url, headers=None, data=None, anonymous=False, gentle=False):
    return request("POST", url, headers=headers, data=data, anonymous=anonymous, gentle=gentle)

def put(url, headers=None, data=None, anonymous=False, gentle=False):
    return request("PUT", url, headers=headers, data=data, anonymous=anonymous, gentle=gentle)

def delete(url, headers=None, anonymous=False, gentle=False):
    return request("DELETE", url, headers=headers, anonymous=anonymous, gentle=gentle)

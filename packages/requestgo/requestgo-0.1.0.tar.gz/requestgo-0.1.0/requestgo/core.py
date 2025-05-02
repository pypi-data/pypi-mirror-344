
import socket
import ssl
from .response import Response
from .utils import parse_url

def _build_request(method, host, path, headers, body=None):
    request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"
    for k, v in headers.items():
        request += f"{k}: {v}\r\n"
    if body:
        request += f"Content-Length: {len(body)}\r\n"
    request += "Connection: close\r\n\r\n"
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

def request(method, url, headers=None, data=None):
    host_path, port, use_ssl = parse_url(url)
    host, *path = host_path.split("/")
    path = "/" + "/".join(path)
    headers = headers or {}
    headers.setdefault("User-Agent", "requestgo/0.1")
    req = _build_request(method.upper(), host, path, headers, data)
    raw = _send(host, port, req, use_ssl)
    return Response(raw)

def get(url, headers=None):
    return request("GET", url, headers)

def post(url, headers=None, data=None):
    return request("POST", url, headers, data)

def put(url, headers=None, data=None):
    return request("PUT", url, headers, data)

def delete(url, headers=None):
    return request("DELETE", url, headers)

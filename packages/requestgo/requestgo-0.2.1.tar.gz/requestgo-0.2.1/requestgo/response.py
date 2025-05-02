
try:
    import fast_response
    FAST = True
except ImportError:
    FAST = False

class Response:
    def __init__(self, raw):
        head, _, body = raw.partition('\r\n\r\n')
        self.headers = self._parse_headers(head)
        self.body = body
        self.status_code = fast_response.status_code(head) if FAST else int(head.split(' ')[1])
        self.text = body

    def _parse_headers(self, head):
        lines = head.split('\r\n')[1:]
        return dict(line.split(': ', 1) for line in lines if ': ' in line)

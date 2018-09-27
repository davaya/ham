import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from actuator import actuator


class MimeTypeParser:
    def __init__(self, v):
        type = 0

class HamHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    hmap = [
        ('correlation_id', 'x-correlation-id'),
        ('created', 'date'),
        ('from', 'authorization'),
        ('to', 'to')
    ]

    def do_GET(s):
        print('GET: Path =', s.path)
        if s.path != '/api':
            s.send_error(404)
            return
        hdrs = {h[0].lower(): h[1] for h in s.headers.items()}
        print('HTTP Headers:')
        for k, v in hdrs.items():
            print('  ' + k + ': ' + v)
        if 'content-length' not in hdrs:
            s.send_error(400, message='Missing Request Content')
            return
        length = hdrs['content-length']
        data = s.rfile.read(int(length))
        print('HTTP Content:', data)

        cm = {'content': json.loads(data)}
        for m, h in s.hmap:
            cm[m] = hdrs[h] if h in hdrs else None
        cm['content_type'] = hdrs['content-type'].split('-', 1)[0]
        cm['msg_type'] = 'request'

        rm = actuator(cm)

        s.send_response(rm['status'])
        s.send_header('Content-type', 'text/plain')
        s.end_headers()
        s.wfile.write(b"Hello")


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HamHandler)
    print('Starting Ham server on port', server_address[1])
    httpd.serve_forever()

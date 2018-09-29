import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from actuator import actuator


def date_to_ms(date):
    return 999


def ms_to_date(milliseconds):
    return 'foo GMT'


hdr_map = [
    ('request_id', 'X-Correlation-ID'),
    ('from', 'Authorization'),
    ('to', 'To')
]


class HamHandler(BaseHTTPRequestHandler):

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
        for m, h in hdr_map:
            cm[m] = hdrs[h.lower()] if h.lower() in hdrs else None
        cm['created'] = date_to_ms(hdrs['date']) if 'date' in hdrs else None
        ct = re.match('(\w+)/(\w+)-(\w+)(.*)', hdrs['content-type'])
        cm['content_type'] = ct.group(2)
        cm['msg_type'] = {'cmd': 'request', 'rsp': 'response', 'not': 'notification)'}[ct.group(3)]

        rm = actuator(cm)

        s.send_response(rm['status'])
        mtype = 'rsp'
        s.send_header('Content-type', 'application/' + rm['content_type'] + '-' + mtype + '+json')
        if rm['created']:
            s.send_header('Date', ms_to_date(rm['created']))
        for h in hdr_map:
            if rm[h[0]]:
                s.send_header(h[1], rm[h[0]])
        s.end_headers()
        s.wfile.write(json.dumps(rm['content']).encode('utf8'))


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HamHandler)
    print('Starting Ham server on port', server_address[1])
    httpd.serve_forever()

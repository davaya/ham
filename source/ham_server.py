from http.server import HTTPServer, BaseHTTPRequestHandler


class HamHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        print('GET: Path =', s.path)
        if s.path != '/api':
            s.send_error(404)
        else:
            hdrs = s.headers.items()
            print('Headers:')
            for h in hdrs:
                print('  ' + h[0] + ': ' + h[1])
            length = s.headers.get('content-length')
            data = s.rfile.read(int(length) if length else 0)
            print('Content:', data)
            s.send_response(200)
            s.send_header('Content-type', 'text/plain')
            s.end_headers()
            s.wfile.write(b"Hello")


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HamHandler)
    print('Starting Ham server on port', server_address[1])
    httpd.serve_forever()

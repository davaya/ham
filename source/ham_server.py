from http.server import HTTPServer, BaseHTTPRequestHandler


class HamHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        print('Path =', s.path)
        if s.path != '/api':
            s.send_error(404)
        else:
            s.send_response(200)
            s.send_header('Content-type', 'text/plain')
            s.end_headers()
            s.wfile.write(b"Hello")


if __name__ == '__main__':
    addr = ('', 8000)
    httpd = HTTPServer(addr, HamHandler)
    print('Starting Ham server on port', addr[1])
    httpd.serve_forever()

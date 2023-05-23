from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class Proxy(BaseHTTPRequestHandler):
    # блокировка сайтов
    BLOCKED_SITES = {
        'google.com': '<!DOCTYPE html><html><head><title>Error</title></head><body><h1>Web-site '
                      'blocked</h1></body></html> '
    }

    def do_GET(self):
        print('Completing GET request')
        print(self.path)

        HEADER_HOST = self.headers['Host']
        for bloked_site in self.BLOCKED_SITES:
            print(bloked_site)
            if bloked_site in HEADER_HOST:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.BLOCKED_SITES[bloked_site].encode())
                return
        conn = HTTPConnection(HEADER_HOST)
        conn.request("GET", self.path)
        resp = conn.getresponse()
        resp_data = resp.read()
        self.print_info(str(HEADER_HOST), str(self.path), resp_data.decode('1251'))
        modified_resp_data = resp_data.replace(b'<title>', b'<title>Modified - ')
        self.send_response(resp.status)
        for header, value in resp.getheaders():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(modified_resp_data if modified_resp_data else resp_data)
        conn.close()

    def print_info(self, host, path, data):
        print('---------------------------------------')
        print('Host: ' + host)
        print('Path: ' + path)
        print('Data: ' + data)
        print('---------------------------------------')


if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), Proxy)
    print(f"Proxy server listen ing on port {PORT}")
    server.serve_forever()

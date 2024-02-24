from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
from http import HTTPStatus
from sockets import SocketServer
import pathlib

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        else:
            file_path = pathlib.Path().joinpath(pr_url.path[1:])
            if file_path.exists():
                self.send_static_file(file_path)
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        
        sockets.process_message(data_dict)

        self.send_response(HTTPStatus.FOUND)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static_file(self, file_path, status=200):
        self.send_response(status)
        content_type = 'text/css' if file_path.suffix == '.css' else 'image/png'
        self.send_header('Content-type', content_type)
        self.end_headers()
        with open(file_path, 'rb') as fd:
            self.wfile.write(fd.read())

def run_http_server():
    server_address = ('', 3000)
    http = HTTPServer(server_address, HttpHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    sockets = SocketServer() 
    http_thread = threading.Thread(target=run_http_server)
    socket_thread = threading.Thread(target=sockets.run_socket_server)

    http_thread.start()
    socket_thread.start()

    http_thread.join()
    socket_thread.join()

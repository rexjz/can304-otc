from http.server import HTTPServer, BaseHTTPRequestHandler
import http
import argparse
import os

server_store = './client_store/'

parser = argparse.ArgumentParser(
    prog='CAN 304 Demo Server',
    description=
    'This is the demo server used to verify One Time Cookie for can304 group project of Group 32',
)


def get_server_store():
    if not os.path.exists(server_store):
        os.makedirs(server_store)
    return server_store


def process_request(request):
    print(request)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/text')
        self.end_headers()
        self.wfile.write("need login".encode('utf-8'))

    def do_POST(self):
        self.send_response(200)



def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()

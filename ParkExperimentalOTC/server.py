import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import hashlib

client_store = './server_store/'


def get_server_store():
    if not os.path.exists(client_store):
        os.makedirs(client_store)
    return client_store


def save_otc(user_name, otc):
    None


def verify_otc(user_name, otc):
    return False


class MyRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("\n\n##############################")
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        otc = self.headers['OTC']
        logging.info("otc verification: " + str(verify_otc("admin", otc)))
        save_otc("admin", otc)

    def do_POST(self):
        logging.info('POST')
        content_length = int(self.headers['Content-Length'])
        otc = self.headers['OTC']
        post_data = self.rfile.read(content_length)
        user_info = json.loads(post_data)
        user_name = user_info['UserName']
        save_otc(user_name, otc)
        logging.info(json.loads(post_data))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping server...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

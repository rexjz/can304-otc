import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import hashlib


def get_bytes_md5(bytes):
    md5 = hashlib.md5()
    md5.update(bytes)
    return md5.hexdigest()


def get_str_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


def int_to_byte(value):
    digit = math.ceil(value.bit_length() / 8)
    return value.to_bytes(digit, 'big')


client_store = './server_store/'


def get_server_store():
    if not os.path.exists(client_store):
        os.makedirs(client_store)
    return client_store


def save_otc(user_name, otc):
    if os.path.exists(os.path.join(get_server_store(), "otc.json")):
        with open(os.path.join(get_server_store(), "otc.json"), "r") as file:
            otc_dict = json.loads(file.read())
    else:
        otc_dict = {}

    with open(os.path.join(get_server_store(), "otc.json"), "w") as file:
        otc_dict[user_name] = otc
        file.write(json.dumps(otc_dict, indent=4))
        logging.info("otc saved")


def verify_otc(user_name, x, y):
    with open(os.path.join(get_server_store(), "otc.json"), "r") as file:
        otc_dict = json.loads(file.read())
        last_x = otc_dict[user_name]
        if y == get_bytes_md5(int_to_byte(int(last_x, 16) | int(x, 16))):
            return True
        else:
            return False


class MyRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("\n\n##############################")
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        otc = self.headers['OTC']
        otc_fields = otc.split(";")
        if not verify_otc(otc_fields[0], otc_fields[1], otc_fields[2]):
            self.send_response(403)
            logging.info("otc verification Fails")
        else:
            logging.info("otc verification Succeeds")
            save_otc(otc_fields[0], otc_fields[1])
            self._set_response()
            self.wfile.write("auth succeeds".encode('utf-8'))

    def do_POST(self):
        logging.info('POST')
        content_length = int(self.headers['Content-Length'])
        otc = self.headers['OTC']
        post_data = self.rfile.read(content_length)
        user_info = json.loads(post_data)
        user_name = user_info['UserName']
        otc_fields = otc.split(";")
        save_otc(otc_fields[0], otc_fields[1])
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

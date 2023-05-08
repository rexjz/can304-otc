import http.client
import json

from hashchain import get_next, generate_hash_chain

h1 = http.client.HTTPConnection('127.0.0.1:8080')


def service():
    while True:
        print("Enter message:")
        x = input()
        h1.putheader("cookie", get_next())
        h1.request(method='GET', url='/', body=x, headers={})
        response = h1.getresponse()
        print('response from server:')
        print(response.headers)


def login():
    print("user name:")
    usr = input()
    print("password:")
    pwd = input()
    generate_hash_chain(123)
    headers = {
        "OTC": get_next()
    }
    h1.request(
        method='POST',
        url='/',
        body=json
            .dumps({
                'UserName': usr,
                'PWD': pwd,
        }).encode('utf-8'),
        headers=headers
    )
    response = h1.getresponse()
    print('response from server:')
    print(response.read())


login()
# service()

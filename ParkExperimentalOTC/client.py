import http.client
import json

from hashchain import get_next, generate_hash_chain, getSeed, get_str_md5

h1 = http.client.HTTPConnection('127.0.0.1:8080')


def service():
    while True:
        print("Enter message:")
        x = input()
        h1.request(method='GET', url='/', body=x, headers={
            "OTC": get_next()
        })
        response = h1.getresponse()
        print('response from server:')
        print(response.read())


def login():
    print("user name:")
    usr = input()
    print("password:")
    pwd = get_str_md5(input())
    generate_hash_chain(getSeed())
    x, y = get_next()
    headers = {
        "OTC": x + "," + y
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
service()

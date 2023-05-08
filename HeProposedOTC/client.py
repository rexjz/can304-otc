import http.client
import json

from hashchain import get_next, generate_hash_chain, getSeed, get_str_md5

h1 = http.client.HTTPConnection('127.0.0.1:8080')

user_name = ""


def get_next_OTC():
    global user_name
    x, y = get_next()
    return user_name + ";" + x + ";" + y


def service():
    while True:
        print("Enter message:")
        x = input()
        h1.request(method='GET', url='/', body=x, headers={
            "OTC": get_next_OTC()
        })
        response = h1.getresponse()
        print('response from server:')
        print(response.read())


def login():
    global user_name
    print("user name:")
    user_name = input()
    print("password:")
    pwd = get_str_md5(input())
    x, y = generate_hash_chain(getSeed())
    headers = {
        "OTC": user_name + ";" + x + ";" + y
    }
    h1.request(
        method='POST',
        url='/',
        body=json
            .dumps({
            'UserName': user_name,
            'PWD': pwd,
        }).encode('utf-8'),
        headers=headers
    )
    response = h1.getresponse()
    print('response from server:')
    print(response.read())


login()
service()

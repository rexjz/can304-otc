import http.client
from hashchain import get_next, generate_hash_chain

h1 = http.client.HTTPConnection('127.0.0.1:8000')


def service():
    while True:
        print("Enter message:")
        x = input()
        h1.putheader("cookie", get_next())
        h1.request(method='GET', url='/', body=x, headers= {})
        response = h1.getresponse()
        print('response from server:')
        print(response.headers)


def login():
    print("user name:")
    x = input()
    print("user name:")
    x = input()

service()
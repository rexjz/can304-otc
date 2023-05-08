import hashlib
import json
import math
import os.path
import random
import sys
client_store = './client_store/'


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


def get_client_store():
    if not os.path.exists(client_store):
        os.makedirs(client_store)
    return client_store


def get_next():
    with open(os.path.join(get_client_store(), "chain.json"), "r") as file:
        dict = json.loads(file.read())
        pointer = dict['pointer']
        y_chain = dict['y_chain']
        x_chain = dict['x_chain']
        x = get_str_md5(str(getSeed()))
        y = get_bytes_md5(int_to_byte(int(x_chain[pointer], 16) | int(x, 16)))
        print("y: " + y + " = " + x + " | " + x_chain[pointer - 1])
        x_chain.append(x)
        y_chain.append(y)
        dict['pointer'] = dict['pointer'] + 1

    with open(os.path.join(get_client_store(), "chain.json"), "w") as file:
        file.write(json.dumps(dict, indent=4))

    return x_chain[pointer + 1], y


def get_initial():
    with open(os.path.join(get_client_store(), "chain.json"), "r") as file:
        dict = json.loads(file.read())
        x = dict['x_chain'][dict['pointer']]
        y = dict['y_chain'][dict['pointer']]
        dict['pointer'] = dict['pointer'] + 1

    with open(os.path.join(get_client_store(), "chain.json"), "w") as file:
        file.write(json.dumps(dict, indent=4))
    return x, y


def generate_hash_chain(seed: int):
    x_chain = []
    y_chain = []
    seed_md5 = hashlib.md5()
    seed_md5.update(str(seed).encode('utf-8'))
    x = seed_md5.hexdigest()
    x_chain.append(x)
    hl = hashlib.md5()
    hl.update(int_to_byte(int(x, 16)))
    y_chain.append(hl.hexdigest())
    json_object = json.dumps({
        'pointer': 0,
        'x_chain': x_chain,
        'y_chain': y_chain
    }, indent=2)
    with open(os.path.join(get_client_store(), "chain.json"), "w") as outfile:
        outfile.write(json_object)


def getSeed():
    return int(random.random() * sys.maxsize)


print(get_next())




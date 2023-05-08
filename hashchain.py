import hashlib
import json
import os.path

client_store = './client_store/'


def get_client_store():
    if not os.path.exists(client_store):
        os.makedirs(client_store)
    return client_store


def get_next():
    dict = {}
    with open(os.path.join(get_client_store(), "chain.json"), "r") as file:
        dict = json.loads(file.read())
        res = dict['chain'][dict['pointer']]
        dict['pointer'] = dict['pointer'] + 1

    with open(os.path.join(get_client_store(), "chain.json"), "w") as file:
        file.write(json.dumps(dict, indent=4))

    return res


def generate_hash_chain(seed: int, length=1000):
    chain = []
    current = str(seed)
    for counter in range(0, length):
        hl = hashlib.md5()
        hl.update(current.encode('utf-8'))
        chain.append(hl.hexdigest())
        current = hl.hexdigest()
    print('hash chain generated', chain)
    chain.reverse()
    json_object = json.dumps({
        'pointer': 0,
        'chain': chain
    }, indent=2)
    with open(os.path.join(get_client_store(), "chain.json"), "w") as outfile:
        outfile.write(json_object)


# generate_hash_chain(123)
# print(get_next())
__author__ = 'Jeremy Rabasco'

import pickle
from Crypto.Cipher import AES
import os
import hashlib
from modules.storable import Storable


__BLOCK_SIZE = 32
__PADDING = b'#'


def __pad(s: bytes) -> bytes:
    return s + (__BLOCK_SIZE - len(s) % __BLOCK_SIZE) * __PADDING


def __encode(aes: AES, clear_text: bytes) -> bytes:
    return aes.encrypt(__pad(clear_text))


def __decode(aes: AES, cipher_text: bytes) -> bytes:
    return aes.decrypt(cipher_text).rstrip(__PADDING)


def write(secret: str, obj: Storable, path: str="default"):
    dirs = '/'.join(path.split('/')[:-1])
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    with open(path, "wb+") as out_file:
        aes = generate_aes(secret)
        out_file.write(__encode(aes, pickle.dumps(obj)))


def generate_aes(secret: str) -> AES:
    sha = hashlib.sha256()
    sha.update(secret.encode())
    key = sha.digest()
    return AES.new(key)


def read(secret: str, obj: Storable, path: str):
    with open(path, "rb") as in_file:
        aes = generate_aes(secret)
        tmp = pickle.loads(__decode(aes, in_file.read()))
        data = {}
        for attr in dir(obj):
            data[attr] = getattr(tmp, attr)
        obj.load(data)


def delete(path: str):
    os.remove(os.getcwd() + '/' + path)
#!/bin/python3.4
__author__ = 'Jeremy Rabasco'

import pickle
from Crypto.Cipher import AES
import os
import hashlib


def generate_aes(secret: str) -> AES:
        hash = hashlib.sha256()
        hash.update(secret.encode())
        key = hash.digest()
        return AES.new(key)


class Storage:

    __BLOCK_SIZE = 32
    __PADDING = b'#'

    def __pad(self, s: bytes) -> bytes:
        return s + (self.__BLOCK_SIZE - len(s) % self.__BLOCK_SIZE) * self.__PADDING

    def __encode(self, aes: AES, clear_text: bytes) -> bytes:
        return aes.encrypt(self.__pad(clear_text))

    def __decode(self, aes: AES, cipher_text: bytes) -> bytes:
        return aes.decrypt(cipher_text).rstrip(self.__PADDING)

    def write(self, secret: str, obj, path: str="default"):
        dirs = '/'.join(path.split('/')[:-1])
        if dirs != "":
            os.makedirs(dirs, exist_ok=True)
        with open(path, "wb+") as out_file:
            aes = generate_aes(secret)
            out_file.write(self.__encode(aes, pickle.dumps(obj)))

    def read(self, file: str, to_fill, secret: str):
        with open(file, "rb") as in_file:
            aes = generate_aes(secret)
            tmp = pickle.loads(self.__decode(aes, in_file.read()))
            data = {}
            for attr in dir(to_fill):
                data[attr] = getattr(tmp, attr)
            to_fill.load(data)

if __name__ == "__main__":
    from service import Service
    print("Writing custom service and re-reading it...", end="")
    service = Service()
    service.service_name = "Hello"
    service.username = "This"
    service.password = "Works"
    storage = Storage()
    storage.write("test", service, "test.serv")
    service2 = Service()
    storage.read("test.serv", service2, "test")
    assert service2.service_name == service.service_name
    assert service2.username == service.username
    assert service2.password == service.password
    os.remove(os.getcwd() + "/test.serv")
    print(" OK")
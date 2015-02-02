#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import pickle
from Crypto.Cipher import AES
import os

BLOCK_SIZE = 32
PADDING = b'{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: c.encrypt(pad(s))
DecodeAES = lambda c, e: c.decrypt(e).rstrip(PADDING)

# generate a random secret key
secret = b'1111111 1111111 1111111 1111111 '

# create a cipher object using the random secret
cipher = AES.new(secret)

class Service:

    def __init__(self, service_name: str="ServiceName", username: str="Username", password: str="Password"):
        self.__service_name = service_name
        self.__username = username
        self.__password = password

    @property
    def service_name(self) -> str:
        return self.__service_name

    @service_name.setter
    def service_name(self, service_name: str):
        self.__service_name = service_name

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = password

    def write(self, file: str=""):
        if file == "":
            file = self.service_name
        with open(file, "wb+") as out_file:
            out_file.write(EncodeAES(cipher, pickle.dumps(self)))

    def read(self, file: str):
        with open(file, "rb") as in_file:
            tmp = pickle.loads(DecodeAES(cipher, in_file.read()))
            self.service_name = tmp.service_name
            self.username = tmp.username
            self.password = tmp.password

if __name__ == "__main__":
    ref_service = Service()
    print("Creation of service with no argument :", end="")
    service1 = Service()
    assert service1.service_name == ref_service.service_name
    assert service1.username == ref_service.username
    assert service1.password == ref_service.password
    print(" OK")

    print("Creation of service with arguments :", end="")
    service1 = Service("service", "user", "pass")
    assert service1.service_name == "service"
    assert service1.username == "user"
    assert service1.password == "pass"
    print(" OK")

    print("Modifying service attributes :", end="")
    service1 = Service()
    service1.service_name = "ser"
    service1.username = "use"
    service1.password = "pas"
    assert service1.service_name == "ser"
    assert service1.username == "use"
    assert service1.password == "pas"
    print(" OK")

    print("Writing to file and retrieving :", end="")
    service1 = Service()
    service1.service_name = "ser"
    service1.username = "use"
    service1.password = "pas"
    service1.write("test")
    service2 = Service()
    service2.read("test")
    assert service1.service_name == service2.service_name
    assert service1.username == service2.username
    assert service1.password == service2.password
    os.remove(os.getcwd()+"/test")
    print(" OK")
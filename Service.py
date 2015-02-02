#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'


class Service:

    def __init__(self, service_name: str="ServiceName", username: str="Username", password: str="Password"):
        self.__service_name = service_name
        self.__username = username
        self.__password = password

    @property
    def service_name(self) -> str:
        return self.__service_name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    def print(self):
        print("Service name :", self.service_name)
        print("Username :", self.username)
        print("Password :", self.password)


if __name__ == "__main__":
    print("Creation of service with no arguments...")
    service1 = Service()
    assert service1.service_name == "ServiceName"
    assert service1.username == "Username"
    assert service1.password == "Password"
    print("...passed.")

    print("Creation of service with arguments...")
    service1 = Service("service", "user", "pass")
    assert service1.service_name == "service"
    assert service1.username == "user"
    assert service1.password == "pass"
    print("...passed.")
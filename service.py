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

    def load(self, data :dict):
        self.service_name = data["service_name"]
        self.username = data["username"]
        self.password = data["password"]

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

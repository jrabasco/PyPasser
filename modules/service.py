__author__ = 'Jeremy Rabasco'

from modules import storable


class Service(storable.Storable):

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

    def load(self, data: dict):
        self.service_name = data["service_name"]
        self.username = data["username"]
        self.password = data["password"]

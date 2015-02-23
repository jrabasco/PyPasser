__author__ = 'Jeremy Rabasco'

from modules import storable
from modules.service import Service


class Database(storable.Storable):
    def __init__(self, name: str="Database"):
        self.__name = name
        self.__services = []

    @property
    def services(self) -> list:
        return self.__services

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    def add_service(self, new_service: Service):
        self.__services.append(new_service)

    def remove_service(self, index: int):
        del self.__services[index]

    def load_service(self, index: int, data: dict):
        self.__services[index].load(data)

    def load(self, data: dict):
        self.__name = data["name"]
        self.__services = data["services"][:]

    def export(self) -> dict:
        res = {
            "name": self.name,
            "services": self.services
        }
        return res
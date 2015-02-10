__author__ = 'Jeremy Rabasco'

import storable
from service import Service


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
        self.__services.remove(index)

    def load(self, data: dict):
        self.__name = data["name"]
        self.__services = data["services"][:]
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

    def load(self, data: dict):
        self.__name = data["name"]
        self.__services = data["services"][:]

    def display(self):
        print("Database", self.__name)
        print("Contains", len(self.__services), "service" + ("s." if len(self.__services) > 1 else '.'))
        for serv in self.__services:
            print()
            print('\t' + serv.service_name)
            print("\tUsername :", serv.username)
            print("\tPassword :", serv.password)
        print()
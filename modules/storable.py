__author__ = 'Jeremy Rabasco'

from abc import ABCMeta, abstractmethod


class Storable(metaclass=ABCMeta):

    @abstractmethod
    def load(self, data: dict):
        """This method should properly load the data from the dictionary"""
        pass

    @abstractmethod
    def export(self) -> dict:
        """This method should properly export data to a dictionary"""
        pass
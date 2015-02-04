__author__ = 'Jeremy Rabasco'

import abc


class Storable:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load(self, data: dict):
        """This method should properly load the data in the dictionary"""
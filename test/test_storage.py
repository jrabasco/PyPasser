#!/usr/bin/python3.4
__author__ = "Jeremy Rabasco"

import sys
import os
sys.path.append("..")
import unittest
from modules import storage
from modules.service import Service
from modules.database import Database


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.service = Service()
        self.database = Database()
        open("test.service", "w+").close()
        open("test.db", "w+").close()

    def test_write_read_service(self):
        self.service.service_name = "Hello"
        self.service.username = "This"
        self.service.password = "Works"

        storage.write("test", self.service, "test.service")
        service2 = Service()
        storage.read("test", service2, "test.service")
        self.assertEqual(service2.service_name, self.service.service_name)
        self.assertEqual(service2.username, self.service.username)
        self.assertEqual(service2.password, self.service.password)

    def test_write_read_database(self):
        self.database.add_service(Service())
        self.database.add_service(Service())
        self.database.name = "Hey"

        storage.write("test", self.database, "test.db")
        database2 = Database()
        storage.read("test", database2, "test.db")
        self.assertEqual(database2.name, self.database.name)
        for i in range(len(self.database.services)):
            self.assertEqual(database2.services[i].service_name, self.database.services[i].service_name)
            self.assertEqual(database2.services[i].username, self.database.services[i].username)
            self.assertEqual(database2.services[i].password, self.database.services[i].password)

    def tearDown(self):
        os.remove(os.getcwd() + "/test.service")
        os.remove(os.getcwd() + "/test.db")

if __name__ == "__main__":
    unittest.main()
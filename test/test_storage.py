#!/usr/bin/python3.4
__author__ = "Jeremy Rabasco"

import sys,os
sys.path.append("..")
import unittest
import storage
from service import Service

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.service = Service()
        open("test.serv", "w+").close()

    def test_write_read_service(self):
        self.service.service_name = "Hello"
        self.service.username = "This"
        self.service.password = "Works"
        storage1 = storage.Storage()
        storage1.write("test", self.service, "test.serv")
        service2 = Service()
        storage1.read("test.serv", service2, "test")
        self.assertEqual(service2.service_name, self.service.service_name)
        self.assertEqual(service2.username, self.service.username)
        self.assertEqual(service2.password, self.service.password)

    def tearDown(self):
        os.remove(os.getcwd() + "/test.serv")

if __name__ == "__main__":
    unittest.main()
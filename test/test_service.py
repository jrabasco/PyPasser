#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'

import sys
sys.path.append("..")
import unittest
from modules import service


class ServiceTest(unittest.TestCase):

    def setUp(self):
        self.ref_service = service.Service()

    def test_simple_service(self):
        service1 = service.Service()
        self.assertEqual(service1.service_name, self.ref_service.service_name)
        self.assertEqual(service1.username, self.ref_service.username)
        self.assertEqual(service1.password, self.ref_service.password)

    def test_custom_service(self):
        service1 = service.Service("service", "user", "pass")
        self.assertEqual(service1.service_name, "service")
        self.assertEqual(service1.username, "user")
        self.assertEqual(service1.password, "pass")

    def test_modifying_service(self):
        service1 = service.Service()
        service1.service_name = "ser"
        service1.username = "use"
        service1.password = "pas"
        self.assertEqual(service1.service_name, "ser")
        self.assertEqual(service1.username, "use")
        self.assertEqual(service1.password, "pas")

    def test_load(self):
        test_service = service.Service()
        test_service.service_name = "Is"
        test_service.username = "This"
        test_service.password = "Working ?"
        test_service2 = service.Service()
        dic = {
            "service_name": test_service.service_name,
            "username": test_service.username,
            "password": test_service.password
        }
        test_service2.load(dic)
        self.assertEqual(test_service.service_name, test_service2.service_name)
        self.assertEqual(test_service.username, test_service2.username)
        self.assertEqual(test_service.password, test_service2.password)

if __name__ == "__main__":
    unittest.main()
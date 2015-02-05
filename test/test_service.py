#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'

import sys
sys.path.append("..")
import unittest
import service


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
        serv = service.Service()
        serv.service_name = "Is"
        serv.username = "This"
        serv.password = "Working ?"
        serv2 = service.Service()
        dic = {}
        dic["service_name"] = serv.service_name
        dic["username"] = serv.username
        dic["password"] = serv.password
        serv2.load(dic)
        self.assertEqual(serv.service_name, serv2.service_name)
        self.assertEqual(serv.username, serv2.username)
        self.assertEqual(serv.password, serv2.password)

if __name__ == "__main__":
    unittest.main()
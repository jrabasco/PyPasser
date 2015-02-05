#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'

import sys
sys.path.append("..")
import unittest
import database
import service


class TestDatabase(unittest.TestCase):

    def test_database_creation(self):
        self.assertEqual(database.Database().name, "Database")

    def test_custom_name(self):
        db = database.Database()
        db.name = "Custom"
        self.assertEqual(db.name, "Custom")

    def test_add_service(self):
        serv = service.Service()
        db = database.Database()
        db.add_service(serv)
        self.assertEqual(serv.service_name, db.services[0].service_name)
        self.assertEqual(serv.username, db.services[0].username)
        self.assertEqual(serv.password, db.services[0].password)

    def test_load(self):
        db = database.Database()
        dic = {}
        dic["name"] = "Hey"
        dic["services"] = [service.Service()]
        db.load(dic)
        self.assertEqual("Hey", db.name)
        self.assertEqual("ServiceName", db.services[0].service_name)
        self.assertEqual("Username", db.services[0].username)
        self.assertEqual("Password", db.services[0].password)

if __name__ == "__main__":
    unittest.main()
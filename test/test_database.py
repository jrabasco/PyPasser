#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'

import sys
sys.path.append("..")
import unittest
from modules import database
from modules import service


class TestDatabase(unittest.TestCase):

    def test_database_creation(self):
        self.assertEqual(database.Database().name, "Database")

    def test_custom_name(self):
        db = database.Database()
        db.name = "Custom"
        self.assertEqual(db.name, "Custom")

    def test_add_service(self):
        test_service = service.Service()
        db = database.Database()
        db.add_service(test_service)
        self.assertEqual(test_service.service_name, db.services[0].service_name)
        self.assertEqual(test_service.username, db.services[0].username)
        self.assertEqual(test_service.password, db.services[0].password)

    def test_load(self):
        db = database.Database()
        dic = {
            "name": "Hey",
            "services": [service.Service()]
        }
        db.load(dic)
        self.assertEqual("Hey", db.name)
        self.assertEqual("ServiceName", db.services[0].service_name)
        self.assertEqual("Username", db.services[0].username)
        self.assertEqual("Password", db.services[0].password)

if __name__ == "__main__":
    unittest.main()
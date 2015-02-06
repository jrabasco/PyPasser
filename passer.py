#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import os
import sys
import storage
import database
import service
import getpass
import logging


def query_yes_no(question: str) -> bool:
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    print(question + " [Y/n] ", end='')
    choice = input().lower()
    if choice in valid:
        return valid[choice]
    else:
        return True


def get_service_data() -> dict:
    print("Enter the new service data:")
    service_name = get_input("Service name: ")
    username = get_input("Username: ")
    password = getpass.getpass()
    return {"service_name": service_name, "username": username, "password": password}


def display_db(db: database.Database):
    print("Database", db.name)
    print("Contains", len(db.services), "service" + ("s." if len(db.services) > 1 else '.'))
    for serv in db.services:
        print('\t' + serv.service_name)
        print("\tUsername :", serv.username)
        print("\tPassword :", serv.password)
        print()


def login(name: str, password: str):
    if not os.path.isdir(os.getcwd() + "/databases"):
        os.mkdir(os.getcwd() + "/databases")
    if not db_exists(name):
        if query_yes_no("Are you willing to create database \"" + name + "\" ?"):
            open("databases/" + name + ".db", "w+").close()
            db = database.Database()
            db.name = name
            db.add_service(create_service())
            storage.write(password, db, "databases/" + name + ".db")
            display_db(db)
    else:
        db = database.Database()
        storage.read(password, db, "databases/" + name + ".db")
        display_db(db)


def db_exists(name: str):
    return os.path.isfile(os.getcwd() + "/databases/" + name + ".db")


def create_service():
    data = get_service_data()
    serv = service.Service()
    serv.load(data)
    return serv


def get_input(msg: str):
    print(msg, end='')
    return input()


def clean_dbs():
    dbs_path = os.getcwd() + "/databases/"
    for (dirpath, dirnames, filenames) in os.walk(dbs_path):
        for file in filenames:
            if file.endswith(".db"):
                if os.stat(dbs_path + file).st_size < 1:
                    os.remove(dbs_path + file)

if __name__ == "__main__":
    try:
        db_name = get_input("Database: ")
        db_pass = getpass.getpass()
        login(db_name, db_pass)
    except Exception:
        logging.exception("FATAL :")
        clean_dbs()
        sys.exit(9000)
    except KeyboardInterrupt as ki:
        print('Interrupted.')
        clean_dbs()
        sys.exit(9000)
#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import os
import sys
import storage
import database
import service
import getpass
import logging
import tkinter


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

    for i in range(len(db.services)):
        print('\t' + str(i+1) + ". " + db.services[i].service_name)
        print("\tUsername :", db.services[i].username)
        #print("\tPassword :", db.services[i].password)
        print()


def login(name: str, password: str) -> database.Database:
    if not os.path.isdir(os.getcwd() + "/databases"):
        os.mkdir(os.getcwd() + "/databases")
    if not db_exists(name):
        if query_yes_no("Are you willing to create database \"" + name + "\" ?"):
            open("databases/" + name + ".db", "w+").close()
            db = database.Database()
            db.name = name
            db.add_service(create_service())
            storage.write(password, db, "databases/" + name + ".db")
            return db
        return None
    else:
        db = database.Database()
        storage.read(password, db, "databases/" + name + ".db")
        return db


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


def get_input_with_choices(msg: str, choices: list):
    done = False
    while not done:
        choice = get_input(msg)
        if choice in choices:
            done = True
        else:
            expected = ','.join(choices)
            print("Not an expected value, expected : " + expected)
    return choice


def clean_dbs():
    dbs_path = os.getcwd() + "/databases/"
    for (dirpath, dirnames, filenames) in os.walk(dbs_path):
        for file in filenames:
            if file.endswith(".db"):
                if os.stat(dbs_path + file).st_size < 1:
                    os.remove(dbs_path + file)


def perform_actions(db: database.Database, password: str):
    cont = True
    while cont:
        services_number = len(db.services)
        choice = get_input_with_choices("What do you want to do ? quit (q), edit database (e), load new db (l), "
                                        "get password (g): ", ['q', 'e', 'l', 'g'])
        if choice == 'q':
            sys.exit(0)
        elif choice == 'e':
            choice = get_input_with_choices("Edit service (e), remove service (r), add service (a), delete db (d), "
                                            "cancel (c): ", ['e', 'r', 'a', 'd', 'c'
            ]).lower()
            if choice == 'e' :
                if services_number > 0:
                    choices = [str(c) for c in range(1, services_number + 1)]
                    choice = get_input_with_choices("Which one (1-" + str(services_number)+"): ",
                                                    choices)
                    data = get_service_data()
                    db.load_service(int(choice) - 1, data)
                    storage.write(password, db, "databases/" + db.name + ".db")
                    display_db(db)
                else:
                    print("No service available.")
            elif choice == 'r':
                if services_number > 0:
                    choices = [str(c) for c in range(1, services_number + 1)]
                    choice = get_input_with_choices("Which one (1-" + str(services_number)+"): ",
                                                    choices)
                    db.remove_service(int(choice) - 1)
                    storage.write(password, db, "databases/" + db.name + ".db")
                    display_db(db)
                else:
                    print("No service available.")
            elif choice == 'a':
                data = get_service_data()
                serv = service.Service()
                serv.load(data)
                db.add_service(serv)
                storage.write(password, db, "databases/" + db.name + ".db")
                display_db(db)
            elif choice == 'd':
                if query_yes_no("Are you sure you want to delete database \"" + db.name + "\" ?"):
                    storage.delete("databases/" + db.name + ".db")
                    del db
                    cont = False
                    if query_yes_no("Quit ?"):
                        sys.exit(0)

        elif choice == 'l':
            del db
            cont = False
        elif choice == 'g':
            if services_number > 0:
                choices = [str(c) for c in range(1, services_number + 1)]
                choice = get_input_with_choices("Which one (1-" + str(services_number)+"): ",
                                                choices)
                r = tkinter.Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append(db.services[int(choice)-1].password)
            else:
                print("No service available.")


def login_prompt() -> (database.Database, str):
    db_name = get_input("Database: ")
    db_pass = getpass.getpass()
    return login(db_name, db_pass), db_pass

if __name__ == "__main__":
    try:
        while True:
            db, password = login_prompt()
            if db is None:
                sys.exit(0)
            display_db(db)
            perform_actions(db, password)
    finally:
        clean_dbs()
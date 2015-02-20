#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import os
import sys
sys.path.append("..")
from modules import storage
from modules import database
from modules import service
import getpass
import tkinter
import pickle

buff_size = 0


def clear():
    global buff_size
    cursor_up_one = '\x1b[1A'
    erase_line = '\x1b[2K'
    print((buff_size + 1)*cursor_up_one)
    for i in range(buff_size):
        print(erase_line)
    print((buff_size + 1)*cursor_up_one)
    buff_size = 0


def query_yes_no(question: str) -> bool:
    global buff_size
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    print(question + " [Y/n] ", end='')
    buff_size += 1
    choice = input().lower()
    if choice in valid:
        return valid[choice]
    else:
        return True


def get_service_data() -> dict:
    global buff_size
    print("Enter the new service data:")
    buff_size += 1
    service_name = get_input("Service name: ")
    username = get_input("Username: ")
    password = get_password()
    return {"service_name": service_name, "username": username, "password": password}


def display_db(db: database.Database):
    global buff_size
    clear()
    print("Database", db.name)
    print("Contains", len(db.services), "service" + ("s." if len(db.services) > 1 else '.'))
    buff_size += 2

    for i in range(len(db.services)):
        print('\t' + str(i+1) + ". " + db.services[i].service_name)
        print("\tUsername :", db.services[i].username)
        print()
        buff_size += 3


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


def get_password():
    global buff_size
    buff_size += 1
    return getpass.getpass()


def get_input(msg: str):
    global buff_size
    buff_size += 1
    return input(msg)


def get_input_with_choices(msg: str, choices: list):
    global buff_size
    done = False
    while not done:
        choice = get_input(msg)
        if choice in choices:
            done = True
        else:
            expected = ','.join(choices)
            print("Not an expected value, expected : " + expected)
            buff_size += 1
    return choice


def clean_dbs():
    dbs_path = os.getcwd() + "/databases/"
    for (dirpath, dirnames, filenames) in os.walk(dbs_path):
        for file in filenames:
            if file.endswith(".db"):
                if os.stat(dbs_path + file).st_size < 1:
                    os.remove(dbs_path + file)


def perform_actions(db: database.Database, password: str):
    global buff_size
    cont = True
    while cont:
        services_number = len(db.services)
        choice = get_input_with_choices("What do you want to do ? quit (q), edit database (e), load new db (l), "
                                        "get password (g): ", ['q', 'e', 'l', 'g'])
        if choice == 'q':
            clear()
            sys.exit(0)
        elif choice == 'e':
            choice = get_input_with_choices("Edit service (e), remove service (r), add service (a), change login "
                                            "information (l), delete db (d), "
                                            "cancel (c): ", ['e', 'r', 'a', 'd', 'c', 'l'])
            if choice == 'e':
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
                    buff_size += 1
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
                    buff_size += 1
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
                choice = get_input_with_choices("Change name (n), password (p), both (b), cancel (c): ",
                                                ['n', 'p', 'b', 'c'])
                name = None
                pword = None

                if choice == 'n':
                    name = get_input("Name: ")
                elif choice == 'p':
                    pword = get_password()
                elif choice == 'b':
                    name = get_input("Name: ")
                    pword = get_password()

                if name is not None or pword is not None:
                    storage.delete("databases/" + db.name + ".db")
                    db.name = name if name is not None else db.name
                    pword = pword if pword is not None else password
                    storage.write(pword, db, "databases/" + db.name + ".db")
                    display_db(db)

        elif choice == 'l':
            del db
            cont = False
            clear()
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
                buff_size += 1


def login_prompt() -> (database.Database, str):
    global buff_size
    db = None
    pass_ok = False
    while not pass_ok:
        try:
            db_name = get_input("Database: ")
            db_pass = get_password()
            db = login(db_name, db_pass)
            pass_ok = True
        except pickle.UnpicklingError:
            clear()
            print("Invalid database name/password combination, try again.")
            buff_size += 1
            pass_ok = False
    return db, db_pass

if __name__ == "__main__":
    try:
        while True:
            db, password = login_prompt()
            if db is None:
                sys.exit(0)
            display_db(db)
            perform_actions(db, password)
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt.")
        pass
    finally:
        clean_dbs()
        try:
            del db
        except NameError:
            pass
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
    password = get_password("Password: ")
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


def get_password(question: str):
    global buff_size
    buff_size += 1
    return getpass.getpass(question)


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
                    name = get_input("New name: ")
                elif choice == 'p':
                    pword = get_password("New password: ")
                elif choice == 'b':
                    name = get_input("New name: ")
                    pword = get_password("New password: ")

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
            return True
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
    return False


def open_db(db_name: str, db_pass: str) -> (database.Database, str):
    db = None
    try:
        if not db_exists(db_name):
            if query_yes_no("Are you willing to create database \"" + db_name + "\" ?"):
                open("databases/" + db_name + ".db", "w+").close()
                db = database.Database()
                db.name = db_name
                db.add_service(create_service())
                storage.write(db_pass, db, "databases/" + db.name + ".db")
        else:
            db = login(db_name, db_pass)
    except (pickle.UnpicklingError, EOFError, ValueError):
        clear()
    return db


def login_prompt():
    return get_input("Database: "), get_password("Password: ")


def handle_login() -> (database.Database, str):
    done = False
    db = None
    while not done:
        db_name, db_pass = login_prompt()
        db = open_db(db_name, db_pass)
        if db is None :
            if not query_yes_no("Could not open any database, retry with another login and password ?"):
                done = True
        else:
            done = True
    return db, db_pass


def list_dbs():
    global buff_size
    dbs = []
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd() + "/databases/"):
        dbs = [file for file in filenames if file.endswith(".db")]
    if len(dbs) < 1:
        print("Not database found.")
        buff_size += 1
    else:
        print(len(dbs), "database" + ("s " if len(dbs) > 1 else ' ') + "found :")
        buff_size += 1 + len(dbs)
        for db in dbs:
            print("\t*", db[:-3])

if __name__ == "__main__":
    try:
        while True:
            action = get_input_with_choices("List databases (l), open/create database (o), quit (q): ", ['l', 'o', 'q'])
            clear()
            if action == 'l':
                list_dbs()
            elif action == 'o':
                continue_db_ops = True
                while continue_db_ops:
                    db, password = handle_login()
                    if db is None:
                        sys.exit(0)
                    display_db(db)
                    continue_db_ops = perform_actions(db, password)
            else:
                sys.exit(0)
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt.")
        pass
    finally:
        clean_dbs()
        clear()
        try:
            del db
        except NameError:
            pass
#!/usr/bin/python3.4

__author__ = "Jeremy Rabasco"

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import sys
import os
sys.path.append("..")
from modules import storage
from modules import database
import pickle

hostName = "localhost"
hostPort = 31415


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        parsed_args = parse_qs(query)
        cleaned_path = urlparse(self.path).path
        path_split = [s for s in cleaned_path.split("/") if len(s) > 0]
        if len(path_split) < 1:
            self.error(400, "No path specified.")
        elif path_split[0] == "databases":
            self.get_databases(parsed_args)
        elif path_split[0] == "list":
            self.get_list()
        else:
            self.error(400, "Invalid path.")

    def get_databases(self, args: dict):
        if "type" in args:
            if args["type"][0] == "ciphered":
                self.__send_raw_db(args)
            elif args["type"][0] == "clear":
                self.__send_clear_db(args)
        else:
            self.error(400, "type not specified")

    def get_list(self):
        dbs = []
        for (dirpath, dirnames, filenames) in os.walk(os.getcwd() + "/databases/"):
            dbs = [file[:-3] for file in filenames if file.endswith(".db")]
        if len(dbs) < 1:
            self.error(404, "No database found.")
        else:
            self.send_ok({"databases": dbs})

    def send(self, code: int,  data: dict):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes_json_from_dict(data))

    def error(self, code: int, message: str):
        self.send(code, {"message": message})

    def send_ok(self, data: dict):
        self.send(200, data)

    def __send_raw_db(self, args: dict):
        if "name" in args:
            code, data, method = self.__get_db_content_to_send(args["name"][0])
            method(code, data)
        else:
            self.error(400, "name not specified")

    def __send_clear_db(self, args: dict):
        if "name" in args:
            if "secret" in args:
                code, data, method = self.__get_db_content_to_send(args["name"][0], args["secret"][0])
                method(code, data)
            else:
                self.error(400, "secret not specified")
        else:
            self.error(400, "name not specified")

    def __get_db_content_to_send(self, db_name: str, secret: str=None) -> (int, object, object):
        if db_exists(db_name):
            if secret is None:
                with open("databases/" + db_name + ".db", "rb") as infile:
                    return 200, {"raw": infile.read().decode("utf-8")}, self.send
            else:
                try:
                    db = database.Database()
                    storage.read(secret, db, "databases/" + db_name + ".db")
                    return 200, db.export(), self.send
                except (pickle.UnpicklingError, EOFError, ValueError):
                    return 403, "denied", self.error
        else:
            return 404, "database not found", self.error


def bytes_json_from_dict(data: dict):
    return bytes(json.dumps(data), encoding="utf-8")


def db_exists(name: str) -> bool:
    return os.path.isfile(os.getcwd() + "/databases/" + name + ".db")


myServer = HTTPServer((hostName, hostPort), MyServer)

print("Server Starts :", hostName, "-", hostPort)

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    print()
    pass

myServer.server_close()
print("Server Stops :", hostName, "-", hostPort)

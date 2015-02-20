#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'
import os


dbs_path = os.getcwd() + "/databases/"
for (dirpath, dirnames, filenames) in os.walk(dbs_path):
    for file in filenames:
        os.remove(dbs_path + file)
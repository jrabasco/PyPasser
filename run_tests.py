#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import os

python_executable = "python3.4"

test_script_name = os.path.basename(__file__)


for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for file in filenames:
        if file.endswith(".py") and file != test_script_name:
            print("Testing", file)
            os.system(python_executable + " " + file)
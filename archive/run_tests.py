#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

import os
import sys

python_executable = "python3.4"

test_script_name = os.path.basename(__file__)

excluded = [test_script_name]
excluded.extend(sys.argv[1:])

print("Files excluded : ", end="")

for script in excluded[:-1]:
    print(script + ", ", end="")

print(excluded[-1] + ".")

print("***")

for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for file in filenames:
        if file.endswith(".py") and file not in excluded:
            print("Testing", file)
            os.system(python_executable + " " + file)
            print("***")
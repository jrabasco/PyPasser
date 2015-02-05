#!/usr/bin/python3.4
__author__ = 'Jeremy Rabasco'

import os
import tkinter

if __name__ == "__main__":
    win = tkinter.Tk()
    db_name_label = tkinter.Label(win, text="Database :")
    db_pass_label = tkinter.Label(win, text="Password :")
    db_name_label.grid(row=0, column=0)
    db_pass_label.grid(row=1, column=0)
    img = tkinter.Image("photo", file="assets/pypasser.png")
    win.tk.call('wm','iconphoto',win._w,img)
    win.mainloop()
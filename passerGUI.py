#!/usr/bin/python3.4

__author__ = 'Jeremy Rabasco'

from tkinter import *
from tkinter import messagebox
import passer


def _query_yes_no(question: str) -> bool:
    return messagebox.askyesno("Confirmation", question)

passer.query_yes_no = _query_yes_no


def entry_event_handler(event):
    if event.keysym == "KP_Enter" or event.keysym == "Return":
        passer.login(db_name_entry.get(), db_pass_entry.get())

win = Tk()
f = Frame(win)
db_name_label = Label(f, text="Database :")
db_name = StringVar()
db_name_entry = Entry(f, textvariable=db_name)
db_name_entry.bind("<Key>", entry_event_handler)
db_pass_label = Label(f, text="Password :")
db_pass = StringVar()
db_pass_entry = Entry(f, textvariable=db_pass, show='*')
db_pass_entry.bind("<Key>", entry_event_handler)
db_name_label.grid(row=0, column=0)
db_name_entry.grid(row=0, column=1)
db_pass_label.grid(row=1, column=0)
db_pass_entry.grid(row=1, column=1)
ok_button = Button(win, text="Open/Create")
ok_button.configure(command=lambda: passer.login(db_name_entry.get(), db_pass_entry.get()))
f.pack()
ok_button.pack()
img = Image("photo", file="assets/pypasser.png")
win.tk.call('wm','iconphoto', win._w, img)
win.wm_title("PyPasser")

win.mainloop()
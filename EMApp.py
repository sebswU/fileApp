"""
Project Data Management App 2021
"""
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import Tk, ttk
from io import StringIO
import re
import json



class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The File App")
        self.geometry("800x450")
        self.resizable(True, True)
        ttk.Label(self, text='Enter thing you want to save (Test)').pack()
        ttk.Entry(self, text='enter something in').pack()
        ttk.Button(self, text='Submit').pack()

if __name__ == "__main__":
     self = MainFrame()
     self.mainloop()

ques = ('log in or sign in')
database = pd.DataFrame()
thing = input(f'enter thing you want to save\n')

def addUsr(usrname, usrRow, database):
    usrname = input('what is your name')
    usrRow = [usrname, 0,"n/a","n/a","n/a",0,0,0]
    usrRow = pd.DataFrame(usrRow)
    with open('cache.json','a') as file:
        fml = pd.read_json(file, 'a')
        fml = fml.append(pd.DataFrame(data=[usrRow]))

    
def dataType(email=False, phone=False, string=False, numberCombo=False):
    if re.findall(r'^([\w\d_-])?@([\w\d_-])?.(org|com)', thing) != []:
        email=True
    elif re.findall(r'^([0-9]{3})?-([0-9]{3})?-([0-9]{4})', thing) != []:
        phone = True
    else:
        if re.findall(r'+\d', thing) != []:
            numberCombo = True
        else:
            string = True

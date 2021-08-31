import csv
import pandas as pd
import os

#asks user what file to open
flag = True
filename = input('what year do you want to access 2016-2019')
if input not in [16,17,18,19]:
    flag = False
    while flag == False:
        filename = input('not a valid file, enter between year 16-19 w/out apostrophe')
        if input in [16,17,18,19]:
            flag = True

with open(f'cbb{filename}.csv', 'r') as file:
    file_manip = pd.read_csv
    file_manip.head()
    file.manip.tail()
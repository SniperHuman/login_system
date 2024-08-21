import csv
import numpy as np
import pandas as pd

pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
data_file = pd.read_csv('costumer_info.csv')

working = True
people_attend = []
print(people_attend)
while working:
    checking_number = 1001
    try:
        checking_person_mail_adress = data_file[data_file["number"] ==checking_number].loc[0,"mail_adress"]
        checking_person_name = data_file[data_file["number"] ==checking_number].loc[0,"name"]
        if checking_person_name not in people_attend:
            people_attend.append(checking_person_name)
            print(people_attend)
        else:
            people_attend.remove(checking_person_name)
        
        working = False
    except:
        pass



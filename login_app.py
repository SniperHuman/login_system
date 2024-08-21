import tkinter as tk
from tkinter import messagebox as mbox

import csv
import numpy as np
import pandas as pd


pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
data_file = pd.read_csv('costumer_info.csv')
names = data_file["name"].tolist()
ids = data_file["id"].tolist()
mailadress = data_file["mail_adress"].tolist()
login_status = data_file["login_status"].tolist()
#costumer_info.csvを読み込んで、名前とiD,mailadressをリスト化する。

    
def register():
    global message
    name_get = name_entry.get()
    email_get = email_entry.get()
    
    try:
        message.pack_forget()
    except:
        pass
    
    if name_get == "" or email_get == "":
        message = tk.Label(window, text="名前もしくはメールアドレスが未入力です。")
        message.pack()
    
    elif email_get.count("@")  == 0:
        message = tk.Label(window, text="無効なメールアドレスです。")
        message.pack()
        
    elif name_get in names and email_get in mailadress:
        message = tk.Label(window, text="この名前とメールアドレスの組み合わせはすでに登録済みです。")
        message.pack()
        
        
    else:
        new_row = {"id":int(ids[-1])+1,"name":name_get,"mail_adress":email_get,"login_status":0}
        data_file.loc[len(data_file)] = new_row
        data_file.to_csv('costumer_info.csv',index=False)
        message = tk.Label(window, text="登録完了です。")
        message.pack()
        
        
        
        
    
        

window = tk.Tk()
window.title("login_system")
window.geometry("300x300")

title = tk.Label(window, text="ログインシステム登録アプリ")
title.pack()

name_text = tk.Label(window, text="名前")
name_entry = tk.Entry(window)
name_text.pack()
name_entry.pack()

email_text = tk.Label(window, text="メールアドレス")
email_entry = tk.Entry(window)
email_text.pack()
email_entry.pack()


register_button = tk.Button(window,text="登録")
register_button["command"] = register
register_button.pack()

window.mainloop()
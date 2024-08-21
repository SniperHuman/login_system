import csv
import numpy as np
import pandas as pd
import cv2
import time
import winsound
import qrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import datetime
# カメラデバイス取得
cap = cv2.VideoCapture(0)
# QRCodeDetectorを生成
try:
    detector = cv2.QRCodeDetector()
except:
    pass
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
data_file = pd.read_csv('costumer_info.csv')
names = data_file["name"].tolist()
ids = data_file["id"].tolist()
#costumer_info.csvを読み込んで、名前とiDをリスト化する。

for i in range(len(names)):
    img = qrcode.make(ids[i])
    img.save(names[i]+'.png')
    #IDをQRコードに紐づけ、作成。そして保存。
    
people_now = []
for i in range(len(names)):
    if data_file[data_file["names"] == names[i]].loc[i,"login_status"] == 1:
        people_now.append(names[i])
    #ファイルのLOGUINSTATUSが１の人をリストに追加.
    

time_to_wait = 3  #新規の読み込み間隔を３秒に設定。
frequency = 2000  # 周波数 (Hz)
duration = 500  # 持続時間 (ミリ秒)

def message_send(mailadress,name,status):
    dt_now = datetime.datetime.now()
    receiver_email = mailadress
    sender_email = "bunnun.login.system202@gmail.com"
    password = "jrauylrbzghybesp"  # 通常のパスワードを使用
    subject = "書道教室文運ログインシステム"
    body = "{}年{}月{}日{}時{}分にお子様が{}しました".format(dt_now.year,dt_now.month,dt_now.day,dt_now.hour,dt_now.minute,status)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # TLS（Transport Layer Security）を開始
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
    



while True:
    ret, frame = cap.read()
    cv2.imshow('Login_system', frame)#画像を出力
    try:
        data = detector.detectAndDecode(frame)#データの読み込み、qrコードで読み取ったiDをリストで返す。
    except:
        pass
    if data[0].isdecimal():#数であるかを判定する、本来QRコードは数字をデータとして持つように作成したが、万が一別のQRコードを読み込んだ時の動作不良をなくすために入れる。
        if data[0] != "" and int(data[0]) in ids:  #何かしらのデータがヒットした時
            checking_id = int(data[0])
            print(checking_id)
            login_mailadress = data_file[data_file["id"] ==checking_id].loc[ids.index(checking_id),"mail_adress"]
            login_name = data_file[data_file["id"] ==checking_id].loc[ids.index(checking_id),"name"]
            login_status = data_file[data_file["id"] ==checking_id].loc[ids.index(checking_id),"login_status"]
            #ログインしている人の名前、id、メールアドレスを一時的に変数に格納。

            if login_status == 0:
                data_file.loc[data_file["id"] == checking_id, "login_status"] = 1
                winsound.Beep(frequency, duration)#音を出力
                message_send(login_mailadress,login_name,"入室")
                #入室時の処理

            elif login_status == 1:
                data_file.loc[data_file["id"] == checking_id, "login_status"] = 0
                winsound.Beep(frequency, duration)#音を出力
                message_send(login_mailadress,login_name,"退室")
                #退出時の処理の処理
                
            #処理内容をもとのｃｓｖファイルに反映
            data_file.to_csv('costumer_info.csv',index=False)
            time.sleep(time_to_wait)#一瞬に入室と退出を繰り返さないように猶予の時間を設定。
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to  quit 
        for x in ids:
           data_file.loc[data_file["id"] == x, "login_status"] = 0 #  システム終了時のログイン状況の初期化
           #処理内容をもとのｃｓｖファイルに反映
           data_file.to_csv('costumer_info.csv',index=False)
        break
    
     
cap.release()
cv2.destroyAllWindows()
#システム終了の処理


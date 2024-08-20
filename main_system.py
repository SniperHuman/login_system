import csv
import numpy as np
import pandas as pd
import cv2
import time
import winsound
import qrcode
from PIL import Image
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

time_to_wait = 3  #新規の読み込み間隔を３秒に設定。
frequency = 2000  # 周波数 (Hz)
duration = 500  # 持続時間 (ミリ秒)
data_get = True 


while True:
    ret, frame = cap.read()
    try:
        data = detector.detectAndDecode(frame)#データの読み込み、qrコードで読み取ったiDをリストで返す。
        data_get = True
    except:
        data_get = False #カメラが接続されていないとき
    if data_get:
        if data[0] != "":  #何かしらのデータがヒットした時
            if data[0].isdecimal():#数であるかを判定する、本来QRコードは数字をデータとして持つように作成したが、万が一別のQRコードを読み込んだ時の動作不良をなくすために入れる。
                cheking_id = int(data[0])
                login_mailadress = data_file[data_file["id"] ==cheking_id].loc[0,"mail_adress"]
                login_name = data_file[data_file["id"] ==cheking_id].loc[0,"name"]
                login_status = data_file[data_file["id"] ==cheking_id].loc[0,"login_status"]
                #ログインしている人の名前、id、メールアドレスを一時的に変数に格納。

            if login_status == 0:
                data_file.loc[data_file["id"] == cheking_id, "login_status"] = 1
                winsound.Beep(frequency, duration)#音を出力
                #入室時の処理

            elif login_status == 1:
                data_file.loc[data_file["id"] == cheking_id, "login_status"] = 0
                winsound.Beep(frequency, duration)#音を出力
                #退出時の処理の処理
                
            #処理内容をもとのｃｓｖファイルに反映
            data_file.to_csv('costumer_info.csv',index=False)
            time.sleep(time_to_wait)#一瞬に入室と退出を繰り返さないように猶予の時間を設定。


        cv2.imshow('Login_system', frame)#画像を出力
        if cv2.waitKey(1) & 0xFF == ord('q'):#press q to  quit
            for x in ids:
                data_file.loc[data_file["id"] == x, "login_status"] = 0
            break
    
     
cap.release()
cv2.destroyAllWindows()
#システム終了の処理
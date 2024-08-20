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


while True:
    ret, frame = cap.read()
    cv2.imshow('Login_system', frame)#画像を出力
    try:
        data = detector.detectAndDecode(frame)#データの読み込み、qrコードで読み取ったiDをリストで返す。
        print(data[0])
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
                #入室時の処理

            elif login_status == 1:
                data_file.loc[data_file["id"] == checking_id, "login_status"] = 0
                winsound.Beep(frequency, duration)#音を出力
                #退出時の処理の処理
                
            #処理内容をもとのｃｓｖファイルに反映
            data_file.to_csv('costumer_info.csv',index=False)
            time.sleep(time_to_wait)#一瞬に入室と退出を繰り返さないように猶予の時間を設定。
    
    if cv2.waitKey(1) & 0xFF == ord('q'):#press q to  quit 
        break
    
     
cap.release()
cv2.destroyAllWindows()
#システム終了の処理


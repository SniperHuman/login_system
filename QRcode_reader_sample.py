import cv2
import time
# カメラデバイス取得
cap = cv2.VideoCapture(0)
# QRCodeDetectorを生成
detector = cv2.QRCodeDetector()
while True:

    ret, frame = cap.read()
    data = detector.detectAndDecode(frame)

    if data[0] != "":
        print(data[0])
        time.sleep(5)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
# 終了処理
cap.release()
cv2.destroyAllWindows()
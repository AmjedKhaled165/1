import cvzone
import cv2
import pygame
import serial
from ultralytics import YOLO
import math
pygame.init()
pygame.mixer.init()
seou=pygame.mixer.Sound(r"C:\Users\Moldu\OneDrive\Dokumente\Arduino\Fire\Sound.mp3")
model = YOLO(r"C:\Users\Moldu\OneDrive\Dokumente\Arduino\Fire\fire.pt")
cap = cv2.VideoCapture(0)

# ser=serial.Serial('COM15',9600)
classname=['fire']

while True:
    ret,frame=cap.read()
    frame2=cv2.resize(frame,(1000,1000))
    res=model(frame2,stream=True)

    for info in res:
        boxes=info.boxes
        for box in boxes:
            con=box.conf[0]
            con=math.ceil(con*100)
            cla = int(box.cls[0])
            if con >50:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),5)
                cvzone.putTextRect(frame,
                                   f'{classname[cla]} {con}%',
                                   [x1+8,y2+100],scale=1.5,
                                   thickness=2)
                # ser.write(b'1')
                # if ser.in_waiting>0:
                #     ard_data=ser.readline().decode().strip()
                #     print('data:',ard_data)
                #     seou.play()
                # else:
                #     seou.stop()
                #     ser.write(b'0')
    cv2.imshow("Amjooooood",frame2)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

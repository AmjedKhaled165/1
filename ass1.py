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






from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')  

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




import cv2
import os
import time

# Set the directory where you want to save the images
save_directory = 'captured_images'
os.makedirs(save_directory, exist_ok=True)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    count = 1
    while True:
        # Capture frame-by frame
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Construct the filename
        filename = os.path.join(save_directory, f"{count}.jpg")

        # Save the image
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

        # Wait for one second before capturing the next image
        time.sleep(1)
        count += 1

except KeyboardInterrupt:
    print("Capture stopped by user.")

finally:
    # Release the camera
    camera.release()
    cv2.destroyAllWindows()



import cv2
import os
import time
from ultralytics import YOLO

# إعداد الدليل الذي ستقوم بتخزين الصور فيه
save_directory = 'captured_images'
os.makedirs(save_directory, exist_ok=True)

# تهيئة الكاميرا
camera = cv2.VideoCapture(0)

# تحقق مما إذا كانت الكاميرا مفتوحة بنجاح
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# تحميل النموذج
model = YOLO('yolov8n.pt')  # استخدم النموذج المناسب

try:
    count = 1
    while True:
        # التقاط إطار
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # بناء اسم الملف
        filename = os.path.join(save_directory, f"{count}.jpg")

        # حفظ الصورة
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

        # تحليل الصورة
        results = model(filename)
        results.print()  # طباعة النتائج

        # الانتظار لمدة ثانية قبل التقاط الصورة التالية
        time.sleep(1)
        count += 1

except KeyboardInterrupt:
    print("Capture stopped by user.")

finally:
    # إطلاق الكاميرا
    camera.release()
    cv2.destroyAllWindows()

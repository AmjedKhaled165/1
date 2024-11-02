https://github.com/garceling/Traffic-Monitoring-on-RPI/tree/main/Run_On_Startup
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




import os
from PIL import Image

# المسار إلى المجلد الذي يحتوي على الصور
folder_path = 'path_to_your_folder'

# الحصول على قائمة بالملفات في المجلد
files = os.listdir(folder_path)

# تصفية الملفات للحصول على الصور وترتيبها
images = sorted(
    [f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))],
    key=lambda x: int(os.path.splitext(x)[0])  # تحويل الاسم إلى عدد صحيح
)

# عرض الصور
for image_file in images:
    image_path = os.path.join(folder_path, image_file)
    img = Image.open(image_path)
    img.show()  # هذا سيفتح الصورة في عارض الصور الافتراضي


from IPython.display import display, Javascript
import cv2
import cvzone
from ultralytics import YOLO
import math

# تحميل نموذج YOLO
model = YOLO('/content/best (1).pt')  # استخدم المسار الصحيح للنموذج

# دالة لالتقاط الفيديو من الكاميرا
def capture_video():
    js = Javascript('''
    async function startVideo() {
        const video = document.createElement('video');
        video.width = 1000;
        video.height = 1000;
        document.body.appendChild(video);
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        video.srcObject = stream;
        video.play();
        return video;
    }
    startVideo();
    ''')
    display(js)

# تشغيل دالة التقاط الفيديو
capture_video()

# قراءة الفيديو من الكاميرا
cap = cv2.VideoCapture(0)

classname = ['fire']

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame2 = cv2.resize(frame, (1000, 1000))
    res = model(frame2, stream=True)

    for info in res:
        boxes = info.boxes
        for box in boxes:
            con = box.conf[0]
            con = math.ceil(con * 100)
            cla = int(box.cls[0])
            if con > 50:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
                cvzone.putTextRect(frame,
                                   f'{classname[cla]} {con}%',
                                   [x1 + 8, y2 + 100], scale=1.5,
                                   thickness=2)

    # عرض الإطار
    cv2_imshow(frame)  # استخدم cv2_imshow لعرض الصورة في Colab
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




import cvzone
import cv2
from ultralytics import YOLO
import math

# تحميل نموذج YOLO
model = YOLO('/content/fire.pt')  # استخدم المسار الصحيح للنموذج

# استخدام ملف فيديو أو كاميرا
cap = cv2.VideoCapture(0)  # استخدم 0 للكاميرا أو استبدله بمسار فيديو

classname = ['fire']

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame2 = cv2.resize(frame, (1000, 1000))
    res = model(frame2, stream=True)
    
    print(res)  # طباعة النتائج لمراقبتها

    for info in res:
        boxes = info.boxes
        for box in boxes:
            con = box.conf[0]
            con = math.ceil(con * 100)
            cla = int(box.cls[0])
            if con > 30:  # تعديل العتبة
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
                cvzone.putTextRect(frame,
                                   f'{classname[cla]} {con}%',
                                   [x1 + 8, y2 + 100], scale=1.5,
                                   thickness=2)

    cv2_imshow(frame)  # استخدم cv2_imshow لعرض الصورة في Colab
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


import cv2
import time
import os
from ultralytics import YOLO

output_video_path = "output_video.mp4"
output_images_path = r"C:\Users\amjdk\Downloads\Smart_Attendence_System\test"
if not os.path.exists(output_images_path):
    os.makedirs(output_images_path)

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))
start_time = time.time()
duration = 20  # مدة التسجيل 20 ثانية

while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    if time.time() - start_time > duration:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

model = YOLO(r"C:\Users\amjdk\Downloads\best.pt")  
cap = cv2.VideoCapture(output_video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # تحليل الإطار فقط كل ثانية
    if frame_count % 20 == 0:  # 20 إطار في الثانية
        results = model(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  
                confidence = box.conf[0]       #
                if confidence > 0.5:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

                    img_name = f"{output_images_path}/detected_frame_{frame_count}.jpg"
                    cv2.imwrite(img_name, frame)  

    frame_count += 1

cap.release()

import cv2
import time
import os
from ultralytics import YOLO

# مسار الفيديو المدمج والصور المخرجة
output_video_path = "output_combined_video.mp4"
output_images_path = r"C:\Users\amjdk\Downloads\Smart_Attendence_System\test"
if not os.path.exists(output_images_path):
    os.makedirs(output_images_path)

# إعداد الفيديو
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (1280, 480))  # 640 * 2 للعرض

# فتح الكاميرتين
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
start_time = time.time()
duration = 20  # مدة التسجيل 20 ثانية

# تسجيل الفيديو المدمج من الكاميرتين
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    
    if not ret1 or not ret2:
        break
    
    # دمج الإطارين جنبًا إلى جنب
    combined_frame = cv2.hconcat([frame1, frame2])
    out.write(combined_frame)
    
    if time.time() - start_time > duration:
        break
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# إغلاق الكاميرات والفيديو المدمج
cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()

# تحميل النموذج
model = YOLO(r"C:\Users\amjdk\Downloads\best.pt")

# تشغيل النموذج على الفيديو المدمج واستخراج الإطارات المعترف بها
cap = cv2.VideoCapture(output_video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # تحليل الإطار كل ثانية (20 إطار في الثانية)
    if frame_count % 20 == 0:
        results = model(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  
                confidence = box.conf[0]
                if confidence > 0.5:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                    
                    img_name = f"{output_images_path}/detected_frame_{frame_count}.jpg"
                    cv2.imwrite(img_name, frame)
    
    frame_count += 1

cap.release()

import RPi.GPIO as GPIO
import time

# تعريف أرقام المنافذ
TRIG = 23
ECHO = 24
LED = 17
IR = 27
BUZZER = 22

# إعداد GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(IR, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)


def get_distance():
    # إرسال نبضة TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # انتظار عودة النبضة
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # حساب المسافة
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")

        if distance > 20:
            GPIO.output(LED, True)
            ir_state = GPIO.input(IR)
            print(f"IR State: {ir_state}")

            if ir_state == 0:
                GPIO.output(BUZZER, True)
            else:
                GPIO.output(BUZZER, False)
        else:
            GPIO.output(LED, False)
            GPIO.output(BUZZER, False)

        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()




##############################################################

from gpiozero import DistanceSensor, LED, Buzzer, InputDevice
from time import sleep

# تعريف الأجهزة
ultrasonic = DistanceSensor(echo=24, trigger=23)
led = LED(17)
ir_sensor = InputDevice(27)
buzzer = Buzzer(22)

try:
    while True:
        distance = ultrasonic.distance * 100  # المسافة بالمتر، نحولها إلى سم
        print(f"Distance: {distance:.2f} cm")

        if distance > 20:
            led.on()
            if not ir_sensor.is_active:
                buzzer.on()
            else:
                buzzer.off()
        else:
            led.off()
            buzzer.off()

        sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")

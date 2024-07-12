# 作者:林翡
# 學號:110916015
# 班級:資四甲
import RPi.GPIO as GPIO
from time import sleep
import  time
import smbus2
from RPLCD.i2c import CharLCD
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# 定義GPIO腳位
led1_pin = 18
led2_pin = 23
led3_pin = 24
trig_pin = 27
echo_pin = 22
buzzer_pin = 25
#設定LCD
sys.modules['smbus'] = smbus2
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
# 初始化GPIO
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led1_pin, GPIO.OUT, initial=0)
    GPIO.setup(led2_pin, GPIO.OUT, initial=0)
    GPIO.setup(led3_pin, GPIO.OUT, initial=0)
    GPIO.setup(trig_pin, GPIO.OUT)  # Trig
    GPIO.setup(echo_pin, GPIO.IN)  # Echo
    GPIO.output(trig_pin, False)  # Set trigger to False (Low)
    GPIO.setup(buzzer_pin, GPIO.OUT)  # Set pins' mode is output
    global Buzz  # Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(buzzer_pin, 440)  # 440 is initial frequency.
    Buzz.start(40)  # Start Buzzer pin with 40% duty ratio

v = 343  # 331+0.6T, T=Celsius

# 超音波測距函式
def detection():
    GPIO.output(trig_pin, GPIO.HIGH)
    sleep(0.00001)  # 10u 秒的TTL觸發信號
    GPIO.output(trig_pin, GPIO.LOW)
    pulse_start = 0
    # ---Response level output have proportional with detection to the distance---
    while GPIO.input(echo_pin) == 0:  # 等待echo_pin變高電平
        pulse_start = time.time()  # 記錄echo引腳變高前的時間點
    while GPIO.input(echo_pin) == 1:  # 等待echo_pin變低電平
        pulse_end = time.time()  # 記錄echo引腳變低前的時間點
    # -----------------------------------------------------------------------------
    # 計算距離
    t = pulse_end - pulse_start
    d = (t * v) / 2
    return d * 100

# 計算三次測量的平均距離
def detection_average():
    d1 = detection()
    sleep(0.065)

    d2 = detection()
    sleep(0.065)

    d3 = detection()
    sleep(0.065)

    distance = (d1 + d2 + d3) / 3
    return distance

# 根據不同距離的判斷，控制Buzzer和三顆LED燈的行為來發出警報
def alarm(distance):
    if distance > 12:
        warning = 0
        Buzz.ChangeDutyCycle(0) # 關閉Buzzer，不發出聲音
        GPIO.output(led3_pin, 0)
        GPIO.output(led1_pin, 1) # 亮第一顆LED燈
        sleep(0.6)
        GPIO.output(led1_pin, 0)
    elif distance <= 12 and distance > 7:
        warning = 0
        Buzz.ChangeDutyCycle(0)
        GPIO.output(led3_pin, 0)
        Buzz.ChangeDutyCycle(50) # 開啟蜂鳴器，設置50%的占空比
        GPIO.output(led2_pin, 1) # 亮第二顆LCD燈
        time.sleep(0.3)
        Buzz.ChangeDutyCycle(0)
        GPIO.output(led2_pin, 0)
    elif distance <= 7 and distance > 2:
        GPIO.output(led3_pin, 1) # 亮第三顆LED燈
        Buzz.ChangeDutyCycle(50)

# 將距離顯示在LCD上
def run_lcd(distance_cm):
    try:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string( "Distance:" )
        lcd.cursor_pos = (1, 0)
        lcd.write_string(str(distance_cm) + " cm" )
    except Exception as exception:
        printException(e=exception, funcName="run_lcd")
        return "Thread end"

def destory():
    Buzz.stop()                 # Stop the buzzer
    GPIO.output(buzzer_pin, 1)      # Set Buzzer pin to High
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        while True:
            for i in range(0, 4, 1):
                distance = detection_average()
                alarm(distance)
                distance1 = round(distance,3) # distance取到小數點第三位
            run_lcd(distance1)
    except KeyboardInterrupt:
        print("\nException: KeyboardInterrupt\n")

    finally:
        destory()
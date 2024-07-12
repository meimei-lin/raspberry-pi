#題目:按按鈕開始測距，並顯示在LCD上
#資四甲-林翡

import sys
import time
import smbus2
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# 定義GPIO的腳位
trigger_pin = 23
echo_pin = 24
btn_pin = 18

press_btn = 1  #按鈕按壓狀態
stopThread = False

#設定LCD
sys.modules['smbus'] = smbus2
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

#初始化GPIO
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT)  # Trigger
    GPIO.setup(echo_pin, GPIO.IN)  # Echo
    GPIO.setup(btn_pin, GPIO.IN, GPIO.PUD_UP)
    GPIO.output(trigger_pin, False)  # Set trigger to False (Low)

#LCD顯示距離的數值
def run_lcd(distance_cm, distance_in):
    try:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string( str(distance_cm) + " cm" )
        lcd.cursor_pos = (1, 0)
        lcd.write_string( str(distance_in) + " in")
    except Exception as exception:
        printException(e=exception, funcName="run_lcd")
        return "Thread end"

def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1

#得到距離的函式
def get_distance():
    GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=pressBtn, bouncetime=200)  # 按鈕按下時觸發 pressBtn 函式
    while True:
        if stopThread:
            lcd.clear()
            print('======= ultra thread stopped ========')
            return "Thread end"
        time.sleep(0.1)

#按鈕按下時的函式(計算距離與顯示在LCD上)
def pressBtn(channel):
    print('Button pressed! Displaying distance...')
    send_trigger_pulse()
    wait_for_echo(True, 5000)
    start = time.time()
    wait_for_echo(False, 5000)
    finish = time.time()
    pulse_len = finish - start
    dis_cm = round(((finish - start) * 34000 / 2), 3)
    dis_in = round(dis_cm * 0.3937, 3)
    run_lcd(dis_cm, dis_in)

if __name__ == '__main__':
    setup()
    try:
        get_distance()
    except KeyboardInterrupt:
        stopThread = True  # 按 Ctrl+C，停止執行緒
        GPIO.cleanup()
           


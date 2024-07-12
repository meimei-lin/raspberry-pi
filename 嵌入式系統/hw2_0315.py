#題目:按按鈕唱小蜜蜂
#資四甲-林翡
import time
import RPi.GPIO as GPIO

#定義GPIO腳位
buzzer = 23
btn = 2

doremi = [523, 587, 659, 349 + 349, 391 + 391]
bee = [doremi[4], doremi[2], doremi[2], doremi[3], doremi[1], doremi[1], doremi[0], doremi[1], doremi[2], doremi[3], doremi[4], doremi[4], doremi[4],
       doremi[4], doremi[2], doremi[2], doremi[3], doremi[1], doremi[1], doremi[0], doremi[2], doremi[4], doremi[4], doremi[2], doremi[1], doremi[1],
       doremi[1], doremi[1], doremi[1], doremi[2], doremi[3], doremi[2], doremi[2], doremi[2], doremi[2], doremi[2], doremi[3], doremi[4], doremi[4],
       doremi[2], doremi[2], doremi[3], doremi[1], doremi[1], doremi[0], doremi[2], doremi[4], doremi[4], doremi[0]]

beat_1 = [1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1,
          1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1,
          1, 2, 1, 1, 2, 1, 1, 1, 1, 1]

#初始化GPIO
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)     # Numbers GPIOs by physical location
    GPIO.setup(btn, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(buzzer, GPIO.OUT)  # Set pins' mode is output
    global Buzz  # Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(buzzer, 440)  # 440 is initial frequency.
    Buzz.start(40)  # Start Buzzer pin with 40% duty ratio

#按鈕回調函式
def my_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)

# 播放音樂函式
def song():
    setup()
    pre = 1  #紀錄按鈕按壓狀態
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=my_callback,bouncetime=200)  
    while True:
        state = GPIO.input(btn)
        if ((not pre) and state) :  #檢查有無按下按鈕
            for i in range(len(bee)):
                Buzz.ChangeFrequency(bee[i])  # Change the frequency along the song note
                time.sleep(beat_1[i] * 0.5)  # delay a note for beat * 0.5s
        GPIO.output(buzzer, False)
        pre = state

def destory():
    Buzz.stop()                 # Stop the buzzer
    GPIO.output(buzzer, 1)      # Set Buzzer pin to High
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':      
    try:
        song()
    except KeyboardInterrupt:   
        destory()  # 按 Ctrl+C 退出時進行清理

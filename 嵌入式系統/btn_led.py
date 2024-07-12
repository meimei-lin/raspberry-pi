import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
led = 23
btn=2

#gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)
gpio.setup(btn,gpio.IN)
pre = 1

try:

    while True:
        state = gpio.input(btn)
        if((not pre) and state):
            gpio.output(led,True)
            sleep(3)
            gpio.output(led,False)
        pre = state
        sleep(0.5)

except KeyboardInterrupt:
    # 當你按下 CTRL+C 中止程式後，所要做的動作
    print("STOP")

except:
    # 其他例外發生的時候，所要做的動作
    print("Other error or exception occurred!")

finally:
    gpio.cleanup()  # 把這段程式碼放在 finally 區域，確保程式中止時能夠執行並清掉GPIO的設定！
   
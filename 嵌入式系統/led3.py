# filename: led1.py
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 18
led2 = 23
led3 = 24

GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)



while True:
   GPIO.output(led1,1)
   GPIO.output(led2,0)
   GPIO.output(led3,0)
   sleep(1) 
   GPIO.output(led1,0)
   GPIO.output(led2,1)
   GPIO.output(led3,0)
   sleep(1)
   GPIO.output(led1,0)
   GPIO.output(led2,0)
   GPIO.output(led3,1)
   sleep(1)

GPIO.cleanup()

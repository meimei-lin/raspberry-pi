import sys
import time
import smbus2



sys.modules['smbus'] = smbus2

from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

try:
    print('Press CTRL + C to quit')
    lcd.clear()
    while True:
        lcd.cursor_pos = (0, 0)
        # lcd.write_string(" 123456789abcdef")
        lcd.write_string("Date: {}".format(time.strftime("%Y/%m/%d")))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Time: {}".format(time.strftime("%H:%M:%S")))
        time.sleep(1)
except KeyboardInterrupt:
    print('Closed Program')
finally:
    lcd.clear()
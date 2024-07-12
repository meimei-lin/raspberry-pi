#題目:(1)LCD 顯示光感(光敏電阻)和搖桿的數值，顯示的格式自己定義。(沒有操作光敏電阻和搖桿)
#    (2)當操作光感(光敏電阻)和搖桿時，顯示當下的數值，同時導引改變的趨勢(例如: UP , DOWN, LEFT, RIGHT, PRESSED, Light, Dark)
#資四甲-林翡
import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadADC(ch):
    if ((ch > 7) or (ch < 0)):
        return -1
    adc = spi.xfer2([1, (8 + ch) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Convert data to voltage level
def ReadVolts(data,deci):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,deci)
    return volts

# Function to determine direction based on joystick position
def GetDirection(vrx_pos, vry_pos):
    center = 1023  # Assuming the center position is 512 for both axes
    threshold = 100  # Sensitivity threshold for direction detection

    # Calculate offsets from the center
   # x_offset = vrx_pos - center
    #y_offset = vry_pos - center

    # Check direction based on offsets
    if vrx_pos == center and vry_pos == center:
        return "Center"
    if vry_pos < center and vry_pos > threshold:
        return "Right"
    if vrx_pos < threshold:
        return "Left"
    if vrx_pos < center:
        return "Down"
    if vry_pos < threshold:
        return "Up"
    return "Unknown"


# Define sensor channels
light_channel = 0
vrx_channel = 1  # Change to channel 1 for X-axis
vry_channel = 2  # Change to channel 2 for Y-axis
swt_channel = 3
# Define delay between readings (s)
delay = 0.5
while True:
    # Read the light sensor data
    light_data = ReadADC(light_channel)
    light_volts = ReadVolts(light_data, 2)
    # Read switch state
    swt_val = ReadADC(swt_channel)
    # Read the joystick position data
    vrx_pos = ReadADC(vrx_channel)
    vry_pos = ReadADC(vry_channel)

    # Get joystick direction
    direction = GetDirection(vrx_pos, vry_pos)
    # Determine if the switch is pressed
    is_pressed = swt_val < 100  # Adjust threshold as needed
    # Print out results
    print("--------------------------------------------")
    print("X : {}  Y : {}  Switch : {}  Direction : {}  Pressed : {} ".format(vrx_pos, vry_pos, swt_val, direction, "Pressed" if is_pressed else "Not Pressed"))
    print("--------------------------------------------")
    # Print out results
    print("    Light : ", light_data, " (", light_volts, "V)")

    # Wait before repeating loop
    time.sleep(delay)

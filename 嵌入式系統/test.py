import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadADC(ch):
    if ((ch > 7) or (ch < 0)):
        return -1
    adc = spi.xfer2([1, (8 + ch) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# Convert data to voltage level
def ReadVolts(data, deci):
    volts = (data * 3.3) / float(1023)
    volts = round(volts, deci)
    return volts


# Function to determine direction based on joystick position
def GetDirection(vrx_pos, vry_pos):
    center = 512  # Assuming the center position is 512 for both axes
    threshold = 50  # Sensitivity threshold for direction detection

    # Calculate offsets from the center
    x_offset = vrx_pos - center
    y_offset = vry_pos - center

    # Check direction based on offsets
    if abs(x_offset) < threshold and abs(y_offset) < threshold:
        return "Center"
    if x_offset > threshold:
        return "Right"
    if x_offset < -threshold:
        return "Left"
    if y_offset > threshold:
        return "Down"
    if y_offset < -threshold:
        return "Up"
    return "Unknown"


# Define sensor channels
light_channel = 0
vrx_channel = 1  # X-axis
vry_channel = 2  # Y-axis
swt_channel = 3  # Switch channel

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
    print(
        f"X: {vrx_pos}  Y: {vry_pos}  Switch: {swt_val}  Direction: {direction}  Pressed: {'Pressed' if is_pressed else 'Not Pressed'}")
    print("--------------------------------------------")
    print(f"Light: {light_data} ({light_volts}V)")

    # Wait before repeating loop
    time.sleep(delay)

    threshold = 800

    # Calculate offsets from the center
    x_offset = vrx_pos - 1023
    y_offset = vry_pos - 1023

    # Check direction based on offsets
    if vrx_pos == 1023 and vry_pos == 1023:
        return "Center"
    if x_offset > threshold and abs(y_offset) < threshold:
        return "Right"
    elif vrx_pos < threshold and abs(y_offset) < threshold:
        return "Left"
    elif y_offset > threshold and abs(x_offset) < threshold:
        return "Down"
    elif vry_pos == 0 and vrx_pos == 1023:
        return "Up"
    else:
        return "Unknown"
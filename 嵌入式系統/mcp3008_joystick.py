import spidev
import time
import os

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 3
vrx_channel = 1
vry_channel = 4

# Define delay between readings (s)
delay = 0.5

while True:
    # Read the joystick position data
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)

    # Read switch state
    swt_val = ReadChannel(swt_channel)

    # Print out results
    print
    "--------------------------------------------"
    print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))

    # Wait before repeating loop
    time.sleep(delay)
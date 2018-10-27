# Monitoring Seabed Dynamics with LoBSTAS
==========

Code for collecting data with the Low-cost Benthic Sensing Trap-Attached System (LoBSTAS). Bootrun.py is a code that will be run on startup, and this is where directions to the Pi will go. GetData.py is where data collection is initiated, while Ready.py displays data collection settings to user for checking before initiating deployment. 

NOTE: Images and videos captured are currently directed to folder (/home/pi/pic and /home/pi/vid), ensure that these folders are created.


## Installation

Install picamera library (https://github.com/waveform80/picamera)

Install neopixel library if you are using the LED ring (https://github.com/jgarff/rpi_ws281x)

To enable bootrun.py on boot, add the following lines to /etc/rc.local before exit 0

    exec 2>> /home/pi/bootlog.log       # add stderr from rc.local to a log file
    exec 1>&2                           # add stdout to same file
    sudo python /home/pi/bootrun.py &   # ensure file path is correct
    
    exit 0
    
## D.O. Sensor calibration and setup
This is for the Atlas Scientific Dissolved Oxygen sensor.

If the sensor board LEd light is not a steady blue color, it needs to be set to i2c mode:

1. Disconnect all wires
2. Connect PGND to TX
3. Connect VCC and ground to board, and wait for LED to turn blue
4. Disconnect power and reconnect all wires

To calibrate to atmospheric concentration:

    from getdata import dosensor
    dosensor().query("CAL")


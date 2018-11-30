# Monitoring Seabed Dynamics with LoBSTAS
==========

Raspberry Pi 3/Zero code for collecting data with the Low-cost Benthic Sensing Trap-Attached System (LoBSTAS), a project birthed at GeotracerKitchen.org. Bootrun.py is a code that will be run on startup, and this is where directions to the Pi will go. GetData.py is where data collection is initiated, while Ready.py displays data collection settings to user for checking before initiating deployment. 

Hackaday Project Logs:
https://hackaday.io/project/160192-lobstas-underwater-camera-sensor


## Installation

Install picamera library (https://github.com/waveform80/picamera). You may download from git and compile or use the eaesier command:
    sudo apt-get install python-picamera

Install neopixel library if you are using the Neopixel LED ring (https://github.com/jgarff/rpi_ws281x)

Install Witty Pi (https://github.com/uugear/Witty-Pi) or WittyPi2 (https://github.com/uugear/Witty-Pi-2) library.

To automatically run bootrun.py on boot, add the following lines to /etc/rc.local before line 'exit 0'

    exec 2>> /home/pi/lobstas/bootlog.log       # add stderr from rc.local to a log file
    exec 1>&2                                   # add stdout to same file
    sudo python /home/pi/lobstas/bootrun.py &   # runs initial python script
    
    exit 0
    
NOTE: Images and videos captured are currently directed to folder (/home/pi/lobstas/pic and /home/pi/lobstas/vid), ensure that these folders exist in the rght directory. Also check for sensor data folder (/home/pi/lobstas/sensor)
    
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
    
## To Collect Data
Login to Pi and navigate to lobstas folder by typing command
    cd /home/pi/lobstas
For testing data collection, type
    sudo python getdata.py
For full, long-term deployment, go to bootrun.py and set deploy=1 in script (this starts data capture whenever the Pi starts up). Then type this command to double check settings:
    sudo python ready.py
    
NOTE: The Pi will auto-shutdown at end of data collection if it is not connected to the Wifi/Hotspot specified in getdata.py (in the power class).

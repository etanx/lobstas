# Monitoring Seabed Dynamics with LoBSTAS
==========

Raspberry Pi 3/Zero code for collecting data with the Low-cost Benthic Sensing Trap-Attached System (LoBSTAS), a project birthed at http://geotracerkitchen.org/. Bootrun.py is a code that will be run on startup, and this is where directions to the Pi will go. GetData.py is where data collection is initiated, while Ready.py displays data collection settings to user for checking before initiating deployment. Additional comments on the functions of the code can be found in the respective scripts.

Hackaday Project Logs:
https://hackaday.io/project/160192-lobstas-underwater-camera-sensor


## Installation
Download code from this repository asn well as dependencies and packages needed.
```
sudo apt-get install git
git clone https://github.com/etanx/lobstas.git
```

Install picamera library (https://github.com/waveform80/picamera). Documentation can be found at https://picamera.readthedocs.io/en/release-1.13/. You may download from git and compile or use the easier command:
```shell
sudo apt-get install python-picamera
```

Install neopixel library if you are using the Neopixel LED ring (https://github.com/jgarff/rpi_ws281x). If you get an error about 'bad zip files', go to https://github.com/jgarff/rpi_ws281x/issues/290 and see solution by hnoesekabel.
```
sudo apt-get install build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
```

Install Witty Pi (https://github.com/uugear/Witty-Pi) or WittyPi2 (https://github.com/uugear/Witty-Pi-2) library. Read WittyPi manual for how to run and program the shell script.
```
wget http://www.uugear.com/repo/WittyPi2/installWittyPi.sh
sudo sh installWittyPi.sh
```

To automatically run bootrun.py on boot and save logs for troubleshooting, type `sudo nano /etc/rc.local` add the following lines to the rc.local script before line 'exit 0'

    exec 2>> /home/pi/lobstas/bootlog.log       # add stderr from rc.local to a log file
    exec 1>&2                                   # add stdout to same file
    sudo python /home/pi/lobstas/bootrun.py &   # runs initial python script
    
    exit 0

    
## D.O. Sensor calibration and setup
This is for the Atlas Scientific Dissolved Oxygen sensor. Read datasheet for full details (https://www.atlas-scientific.com/product_pages/circuits/ezo_do.html).

If the sensor board LED light is not a steady blue color, it needs to be set to i2c mode:

1. Disconnect all wires
2. Connect PGND to TX
3. Connect VCC and ground to board, and wait for LED to turn blue
4. Disconnect power and reconnect all wires

Check if the sensor is connected by typing the command below which should display some i2c addresses if connected properly.
```
sudo i2cdetect -y 1
```
To calibrate to atmospheric concentration eun the following lines:

    from getdata import dosensor
    dosensor().query("CAL")
    
## Data Collection
NOTE: Images and videos captured are currently directed to folder (/home/pi/lobstas/pic and /home/pi/lobstas/vid), ensure that these folders exist in the rght directory. Also check for sensor data folder (/home/pi/lobstas/sensor)

Login to Pi and navigate to lobstas folder by typing command
```shell
cd /home/pi/lobstas
```
For testing data collection, type
```shell
sudo python getdata.py
```
For full, long-term deployment, go to bootrun.py and set deploy=1 in script (this starts data capture whenever the Pi starts up). Then type this command to double check settings:
```shell
sudo python ready.py
```
NOTE: The Pi will auto-shutdown at end of data collection if it is not connected to the Wifi/Hotspot specified in getdata.py (in the power class).

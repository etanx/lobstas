# LoBSTAS data collection, camera/power/memory management script.
# author: Elizabeth H. Tan
# created: 10 August 2018

# Pi Camera code
#     https://github.com/waveform80/picamera
#     Copyright 2013-2017 Dave Jones <dave@waveform.org.uk>

# Atlas Scientific sensor code 
#     https://github.com/AtlasScientific/Raspberry-Pi-sample-code
#     Copyright (c) 2016 AtlasScientific

# Neopixel LED Ring code  
#     https://github.com/jgarff/rpi_ws281x
#     Copyright (c) 2014, jgarff
#     All rights reserved.

import os
import datetime
from picamera import PiCamera  # for camera
from fractions import Fraction # for shutterspeed
import csv # collect sensor data
import RPi.GPIO as GPIO
from neopixel import *

# for AtlasI2C
import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
import time       # used for sleep delay and timestamps
import string     # helps parse strings

# initialize global variable to be displayed in video
DO = 'N/A' 

# create directories for data storage if non-existent
os.system('sudo mkdir -p /home/pi/lobstas/vid')
os.system('sudo mkdir -p /home/pi/lobstas/pic')
os.system('sudo mkdir -p /home/pi/lobstas/sensor')

##############################################################################
# object class for camera pictures and videos
class cam:
    #camera settings
    resolution = (1296,972)       # note: this affects field of view (FOV)
    framerate = 15                 # minimum Fraction(1,6)
    whitebalance = 'auto'          # auto, off, cloudy, fluorescent, flash etc
    exposure = 'nightpreview'	  # auto, nightpreview, backlight, beach etc

    rotate = 180                      # rotate view
    brightness = 50                   # 0-100, default 50
    contrast = 0		      # -100 to 100, default 0
    sharpness = 40		      # 0-100, default 0

    pvscreen = 0	# 1 = deisplayed preview over HDMI monitor
    pvtime = 0.5	# preview time before capture

    #manual settings only if enabled
    manual = 0                 		# set 1 to enable
    ISO = 800                  		# sensitivity 0(auto), max 800
    shutterspeed = Fraction(1,15)         #  0 (auto), max 6s

    vidlength = 15 	# default video length

    settings = ''

    # function to initialize camera
    def setup(self, preview=pvtime, previewscreen=pvscreen,res=resolution,fps=framerate, sh=shutterspeed, iso=ISO, wb=whitebalance,exp=exposure, rot=rotate, sharp=sharpness, cont=contrast, bright=brightness):
	self.camera = PiCamera()
        self.camera.resolution = res
	self.camera.framerate = fps

	if self.manual == 1:		# set manual settings
            self.camera.shutter_speed = sh*1000000
            self.camera.iso = iso
            self.settings = 'ISO' + str(iso) + ' S' + str(sh)
            self.camera.exposure_mode = 'off'
            self.camera.whitebalance = wb
	else:
	    self.camera.exposure_mode = exp
	    self.camera.awb_mode = wb
	    self.settings = 'Exp:' + exp + ' WB:' + wb

        self.camera.rotation = rot
        self.camera.sharpness = sharp
        self.camera.contrast = cont
        self.camera.brightness = bright

        # begin preview if screen attached
	if previewscreen ==1:
        	camera.start_preview()
	time.sleep(preview)			# pauses for preview 

	return (self.camera,self.settings) 

    # function to capture image
    def pic(self,camera,annotate=settings):
    	# captures image
	date = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
	camera.annotate_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + annotate + ' ' + DO + ' mg/L'
  	camera.capture('/home/pi/lobstas/pic/img' + date + '.jpeg')
	print('Captured img' + date[2:17] + '.jpeg')

    # function to capture video
    def vid(self,camera,vidlength=vidlength):
        date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        camera.annotate_text = date + ' ' + DO + ' mg/L'

        try:
            camera.start_recording('/home/pi/lobstas/vid/vid_' + date + '.h264')
            print(date + " Recording started: Ctrl-C to stop...")

            start = datetime.datetime.now()
            while (datetime.datetime.now() - start).seconds < vidlength:
                camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ' + DO + ' mg/L')
                camera.wait_recording(0.2)
            camera.stop_recording()

            end = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            print(end + " Recording complete")
            print('Saved vid' + date[2:17] + '.h264')

        except KeyboardInterrupt:
            camera.stop_recording()
            end = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            print(end + " Recording stopped: Keyboard Interrupt")
	    print("\nSaved vid_" + date[2:17] + '.h264')
        
    def close(self,camera,previewscreen=pvscreen):
        if previewscreen ==1:
		    camera.stop_preview()

    	camera.close()	

# object class for LEd lights
class light:
    sunrise = 6 # hour of sunrise in 24hr format
    sunset = 19 # hour of sunset in 24hr format

    LEDpin = 12 #board GPIO pin number

    R = 255
    G = 190
    B = 190
    
    # function to turn on standard LED ring
    def on(self,pin=LEDpin, set=sunset, rise=sunrise):
	    GPIO.setwarnings(False)
	    GPIO.setmode(GPIO.BOARD)
	    GPIO.setup(pin,GPIO.OUT)

	    # turn on LED for light if sunlight not present
	    d = datetime.datetime.now()
	    if (d.hour >= set or d.hour <= rise):
		    GPIO.output(pin,GPIO.HIGH)	
			
    # function to turn off standard LED ring
    def off(self, pin=LEDpin, set=sunset, rise=sunrise):
	d = datetime.datetime.now()
        if (d.hour >= set or d.hour <= rise):
		GPIO.output(pin,GPIO.LOW)
        GPIO.cleanup()

    # function to turn on neopixel LED ring
    # make sure neopixel library is installed!
    def neopixel(self,R,G,B):    
        # LED strip configuration:
        LED_COUNT      = 16      # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/$
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor$
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        strip.begin()

        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(G,R,B))
            strip.show()

        return


# object class for Atlas Scientific I2C D.O. sensor
class dosensor:
	long_timeout = 1.5         	# the timeout needed to query readings and calibrations
	short_timeout = .5         	# timeout for regular commands
	default_bus = 1         	# the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
	default_address = 97     	# the default address for the sensor
	current_addr = default_address

	dointerval = 2
	doreadings = 5

	def __init__(self, address=default_address, bus=default_bus):
		# open two file streams, one for reading and one for writing
		# the specific I2C channel is selected with bus
		# it is usually 1, except for older revisions where its 0
		# wb and rb indicate binary read and write
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# initializes I2C to either a user specified or default address
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		# set the I2C communications to the slave specified by the address
		# The commands for I2C dev using the ioctl functions are specified in
		# the i2c-dev.h file from i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# appends the null character and sends the string over I2C
		cmd += "\00"
		self.file_write.write(cmd)

	def read(self, num_of_bytes=31):
		# reads a specified number of bytes from I2C, then parses and displays the result
		res = self.file_read.read(num_of_bytes)         # read from the board
		response = filter(lambda x: x != '\x00', res)     # remove the null characters to get the response
		if ord(response[0]) == 1:             # if the response isn't an error
			# change MSB to 0 for all received characters except the first and get a list of characters
			char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
			# NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
			return ''.join(char_list)     # convert the char list to a string and returns it
		else:
			return "Error " + str(ord(response[0]))

	def query(self, string):
		# write a command to the board, wait the correct timeout, and read the response
		self.write(string)

		# the read and calibration commands require a longer timeout
		if((string.upper().startswith("R")) or
			(string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif string.upper().startswith("SLEEP"):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)

		return self.read()

	def close(self):
		self.file_read.close()
		self.file_write.close()


	def poll(self, readings=doreadings,interval=dointerval):
        	# collect data into CSV
        	filename = datetime.datetime.now().strftime("%Y%m%d")
		print('Saving data in do' + filename + '.csv')

        	for i in range (readings):
            	#get DO reading	
            	    try:
    	        	do = self.query("R")
			global DO # set for camera thread to use
			DO = do
            	    except IOError:
    	        	pass
	            	do = '101'
            	    except:
	        	do = '99'

		    d = datetime.datetime.now()

		    # write DO data to file and save
            	    with open('/home/pi/lobstas/sensor/do' + filename + '.csv','ab') as f:
                	writer = csv.writer(f)
                	writer.writerow([do,d.year,d.month,d.day,d.hour,d.minute,d.second])

            	    print(d.strftime("%H_%M_%S ") + do + " mg/L")

		    if interval > self.long_timeout:
			time.sleep(interval-self.long_timeout)


	    	# put device to sleep when done
        	try:    
            		self.query('sleep')
        	except IOError:
            		pass    
		
# object class for power functions
class power:
	
    # power saving for still-functional Pi
    def save():
	    os.system('sudo /usr/bin/tvservice -o')    #disables HDMI
	    os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind") #USB/LAN
	    os.system("sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness'")
	    os.system("sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'")
	    #os.system('ifconfig wlan0 down')   # disables Wifi
	    print('\n')	
	    print('Disabled HDMI, USB, LAN, and LEDs.')

    # checks if lab wifi or hotspot is connected for shutdown
    def wifi():
	    from subprocess import Popen, PIPE
	    pipe = Popen("ip route show | grep 'default' | awk '{print $3}' ",shell=True, stdout=PIPE).stdout
	    wifi_ip = pipe.read()

	    if '10.0.1.1' in wifi_ip:
		    status = 1
		    print('Connected to WiceFi '+wifi_ip)
	    elif '192.168.43.1' in wifi_ip:
		    status=2
		    print('Connected to Mobile  Hotspot ' +wifi_ip)
	    elif wifi_ip == None:
		    status = 0
		    print('No wifi connected.')
	    return status

    # shuts down raspberry pi
    def shutdown(self):
        # try to go to sleep
	    status = self.wifi()
	    if status == 0:
        	print("No Wifi detected. Shutting down...")
        	os.system('sudo halt')


# Create an object class for each storage drive
class StorageDrive:
	def __init__(self,name,path):

		self.name = name
		self.path = path
		# Try to open the USB drives, if you cannot open the drive, 
                #mark as not present and set size availabe as 0
		try:
			usb = os.statvfs(path)
			self.space = (usb.f_frsize * usb.f_bfree)/1024/1024
			self.present = 1
		except:
			self.space = 0
			self.present = 0

# main function to execute data collection
def main():
    # first check for available storage
    min_space = 50 #minimum space required in MB
    local = StorageDrive('root','/')
    print('Storage available = ' + str(local.space) + ' MB')
    print('\n')

    if local.space >= min_space:

        # take pics and vid
        #light().on()          # turns LED light on
        (c,annotate) = cam().setup()
	cam().vid(c)
        cam().pic(c,annotate) #take first picture
	time.sleep(1)
        cam().pic(c,annotate) # take second picture
        cam().close(c)
        #light().off()         # turns LEd light off

    else:
        print('Stopped: Storage reached minimum (' + str(min_space) + ') MB.')
        print('\n')

    #power().shutdown() # MOVED THIS TO ANOTHER EXECUTING SCRIPT

####################################################################################
# run functions if script is called directly
if __name__ == '__main__':
	
    from threading import Thread
    import math
   
    # get number of DO sensor points to match length of video
    points = math.ceil(cam().vidlength / dosensor().dointerval) + 1    
    print("Number of D.O. points to measure: " + str(int(points)))
    
    # start the first thread
    thread1 = Thread(target = dosensor().poll, args = (int(points),))
    thread1.start()
	
    # start the second thread
    thread2 = Thread(target = main, args = ())
    thread2.start()

    # wait for both threads to finish
    thread1.join()
    thread2.join()
    print("Threads complete! Checking for wifi...")
 
    # Checks for WiceFi or ET's Mobile Hotspot
    status = power().wifi

    if status == 0:
	power().shutdown()
    else:
	print("Wifi connected, not shutting down.")

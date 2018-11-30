# checking interface before deployment

from getdata import *
import sys

print("====== CAMERA ======")
print("Resolution: " + str(cam.resolution[0]) + "x" + str(cam.resolution[1]))
print("White Balance: " + cam.whitebalance)
print("Preview time: " + str(cam.pvtime) + "s")

if cam.manual == 1:
	print("Manual ISO: " + str(cam.ISO))
	print("Manual Shutterspeed: " + str(cam.shutterspeed))
else:
	print("Exposure Mode: " + cam.exposure)


print("")
print("====== IMAGE =======")
print("Rotation: " + str(cam.rotate))
print("Brightness: " + str(cam.brightness))
print("Contrast: " + str(cam.contrast))

print("")
print("=====VIDEO=====")
print("Video length: " + str(cam.vidlength) + 's')
print("Framerate: " + str(cam.framerate) + 'fps')


camcheck = raw_input("\nCamera settings correct? (y/n)")

if 'y' in camcheck:
	print("")
else:
	sys.exit("Please edit camera details in getdata.py")



print("==== LIGHTING ====")
print('Sunrise hour ' + str(light.sunrise))
print('Sunset hour ' + str(light.sunset))
print('RGB: ' + str(light.R) + ' ' + str(light.G) + ' ' +  str(light.B))
print('Board pin no.' + str(light.LEDpin))


lightcheck = raw_input("\nLighting settings correct? (y/n)")

if 'y' in camcheck:
        print("")
else:
        sys.exit("Please edit lighting details in getdata.py")


print("")
print("==== DISSOLVED OXYGEN SENSOR ====")
print("Sampling interval: " + str(dosensor.dointerval))
print("Number of readings: " + str(dosensor.doreadings))	
print("Board timeout: " + str(dosensor.long_timeout))
print("i2C bus " + str(dosensor.default_bus))

confirm = raw_input("\nAre all DO details correct? (y/n)")

if 'y' in confirm:
	print(" ")
else:
	sys.exit("Please check sensor details.")


print("WittyPi schedules available:")
print("1) 10 minutes")
print("2) 15 minutes")
print("3) 30 minutes")
print("4) 1 hour")
print("5) Exit")

choice = raw_input("\nChoose sampling interval (1-4):")

if '1' in choice: 
	interv = ('10m')
elif '2' in choice:
	interv = ('15m')
elif '3' in choice:
	interv = ('30m')
elif '4' in choice:
	interv = ('1h')
elif '5' in choice:
	sys.exit("Exiting script.")
else:
	sys.exit("Option not selected.")

print("\nCopying " + interv + " schedule file...")

# copies schedule to witty pi main schedule and executed
try:
	os.system('sudo cp /home/pi/wittyPi/schedules/interval' + interv + '.wpi /home/pi/wittyPi/schedule.wpi')
	os.system('sudo /home/pi/wittyPi/runScript.sh')
except:
	print("Please make sure WittyPi is installed.")

confirm = raw_input("Shutdown for deployment? (y/n)")
if 'y' in confirm:
	print("Ready to go! Shutting down...")
	import os
	os.system('sudo shutdown')
	import time
	time.sleep(60)
else:
	sys.exit("Shut down cancelled.")


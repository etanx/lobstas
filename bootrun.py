# This code will be run on boot from /etc/rc.local

deploy = 1

from time import sleep

if deploy == 1:
	import os
	# script will shut down after completion if no wifi detected
	os.system('sudo python /home/pi/getdata.py')


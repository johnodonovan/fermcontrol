#http://192.168.1.162:25105/3?026206B4690F11FF=I=3

import requests
import time
import os
from requests.auth import HTTPBasicAuth


##temp control variables
#default fermentattion temperature 62. @todo Read this in (in F) with -t param.
target_temp = 62
#overshoot value.  Number of degrees below target value to hit with cooler
offset = 0
#ontime is the number of seconds to run the pump
ontime = 120
#offtime is the number of seconds to wait between runs
offtime = 480
#number of seconds to wait between temp checks.  
frequency = ontime + offtime


#load system drivers
os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')

#to read beer temp in fermenter
temp_sensor1 = '/sys/bus/w1/devices/28-0000065cf01d/w1_slave'
#air temp in fermenter
temp_sensor2 = '/sys/bus/w1/devices/28-0000065cd208/w1_slave'
#to read fridge temp
temp_sensor3 = '/sys/bus/w1/devices/28-0000065cc2d0/w1_slave'

def temp_raw():

    f1 = open(temp_sensor2, 'r')
    lines1 = f1.readlines()
   
    f1.close()
   

    Lines = [lines1]

    return Lines


def read_temp1():
    Lines = temp_raw()
    lines = Lines[0]
    while lines[0].strip()[-3:] != 'YES':

        time.sleep(0.2)

        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:

        temp_string = lines[1].strip()[temp_output+2:]

        temp_c = float(temp_string) / 1000.0

        temp_f = temp_c * 9.0 / 5.0 + 32.0

        #return temp_c, temp_f
        return temp_f


def insteon_direct(ip = "192.168.1.162", port = "25105", username = "AvJOqyPbu0", password = "jod3213211", command = "026206B4690F11FF"):
    auth=HTTPBasicAuth( username, password )
    url = u'http://%s:%s/3?%s=I=3' % ( ip, port, command )
    #utils.log( url )
    print url
    r = requests.post(url=url, auth=auth)

print('controller started')

temp1 = read_temp1()
while(True):	
    #check if temp is within range   
    if  temp1 > (target_temp - offset):
        print "target is %s, temp is %s : pump running for %d seconds" % (target_temp, temp1, ontime) 
        insteon_direct(ip = "192.168.1.162", port = "25105", username = "AvJOqyPbu0", password = "jod3213211", command = "026207B4180F11FF")
        time.sleep(ontime) #turn on for a number seconds
        #fast off
        print "pump off for %r seconds" % offtime
        insteon_direct(ip = "192.168.1.162", port = "25105", username = "AvJOqyPbu0", password = "jod3213211", command = "026207B4180F13FF")
        time.sleep(offtime) #turn off for a number of seconds
    else:   
    	print "target is %r, temp is %r : pump off" % (target_temp, temp1) 
    	time.sleep(frequency)  #read the time again after waking
	
	temp1 = read_temp1()
print('done')
	  

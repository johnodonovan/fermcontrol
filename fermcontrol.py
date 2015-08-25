import plotly.plotly as py
# (*) Useful Python/Plotly tools
import plotly.tools as tls   
 
# (*) Graph objects to piece together plots
from plotly.graph_objs import *
 
import numpy as np  # (*) numpy for math functions and arrays
#import readadc
import os
import glob
import time
# (*) Import module keep track and format current time
import datetime
from datetime import timedelta  #for computing your timezone

from plotly.graph_objs import *



#plot.ly variables
#sign in.  could be done with a credentials file too
username = 'johnodonovan'
api_key = 'qs5mifboo0'
stream_token1 = 'py124k3pbb'
stream_token2 = 'bu928auuho';
stream_token3 = '95tpqngzhz';
stream_token4 = '8r44a0tnm0';

py.sign_in(username, api_key)

#insteon variables
#http://192.168.1.162:25105/3?026206B4690F11FF=I=3



#load system    vtcx
os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')

temp_sensor1 = '/sys/bus/w1/devices/28-0000065cf01d/w1_slave'
temp_sensor2 = '/sys/bus/w1/devices/28-0000065cd208/w1_slave'
temp_sensor3 = '/sys/bus/w1/devices/28-0000065cc2d0/w1_slave'


##temp control variables
#default fermentation temp is 62. @todo Read this in (in F) with -t param.
target_temp = 62

##plotting variables
#number of points to plot on the screen (>10000 is slow on plotly)
history = 5000
#number of seconds to wait between plot points.  Default 60 with 50400 history for a 2 week fermentation plot
plotfrequency = 15
#name of plot
plotname = "FerMonitor-x"


def temp_raw():

    f1 = open(temp_sensor1, 'r')
    f2 = open(temp_sensor2, 'r')
    f3 = open(temp_sensor3, 'r')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    lines3 = f3.readlines()

    f1.close()
    f2.close()
    f3.close()

    Lines = [lines1, lines2, lines3]

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





def read_temp2():
    Lines = temp_raw()
    lines = Lines[1]
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





def read_temp3():
    Lines = temp_raw()
    lines = Lines[2]
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

# Get stream id from stream id list 
#stream_id = stream_ids[0]

# Make instance of stream id object 
stream = Stream(
    token=stream_token1,  # (!) link stream id to 'token' key
    maxpoints=history    # (!) keep a max of 80 pts on screen
)

# Make instance of stream id object 
stream2 = Stream(
    token=stream_token2,  # (!) link stream id to 'token' key
    maxpoints=history    # (!) keep a max of 80 pts on screen
)

stream3 = Stream(
    token=stream_token3,  # (!) link stream id to 'token' key
    maxpoints=history    # (!) keep a max of 80 pts on screen
)

stream4 = Stream(
    token=stream_token4,  # (!) link stream id to 'token' key
    maxpoints=history    # (!) keep a max of 80 pts on screen
)


# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream), 
    name='Ambient'        # (!) embed stream id, 1 per trace
)

trace2 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream2), 
    name='RedBox1'        # (!) embed stream id, 1 per trace
)

trace3 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream3),         # (!) embed stream id, 1 per trace
    name='Target Temp'
)

trace4 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=dict(stream4),         # (!) embed stream id, 1 per trace
    name='MiniFridge'
)
data = Data([trace1,trace2,trace3,trace4])

# Add title and other details to layout object

layout = Layout(
    showlegend=True,
    title='Fermentation Temps :: ShamrockBrew',
    xaxis=XAxis(
        title='Time (Pacific Standard Time)',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=YAxis(
        title='Temp in Degrees Fahrenheit',
        titlefont=Font(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
#unique_url = py.plot(fig, filename=plotname, fileopt='extend')
unique_url = py.plot(fig, filename=plotname, fileopt='new')
print unique_url


# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object

s = None
s2 = None
s3 = None
s4 = None
s = py.Stream(stream_token1)
s2 = py.Stream(stream_token2)
s3 = py.Stream(stream_token3)
s4 = py.Stream(stream_token4)
# (@) Open the stream
s.open()
s2.open()
s3.open()
s4.open()

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(0.5) 


while True:   #change back to N to specify run time limit
    try:    
    # Compute offset for Pacific Time (PST)
    	d1 = datetime.datetime.now()
    	d = timedelta(hours = -7)
    	d2 = d1+d
    	x=d2.strftime('%Y-%m-%d %H:%M:%S')
	# (-) Both x and y are numbers (i.e. not lists nor arrays)

    	# (@) write to Plotly stream!
    	s.write(dict(x=x,y=read_temp1()))  
    	s2.write(dict(x=x,y=read_temp2()))
    	s3.write(dict(x=x,y=target_temp))
        s4.write(dict(x=x,y=read_temp3()))
    	#
    	#(!) Write numbers to stream to append current data on plot,
    	#     write lists to overwrite existing data on plot (more in 7.2).
        time.sleep(plotfrequency)
# #catch exceptions and continue
    except Exception as e:
		print "Unexpected Error: "
		print e.__doc__
		print e.message  
# (@) Close the stream when done plotting
s.close() 
s2.close()
s3.close()
s4.close()



            





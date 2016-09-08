import RPi.GPIO as GPIO
import time
import readchar
import sys
import os
from sys import argv

if len(argv)> 1:
	routine = argv[1]
else:
	print('No routine loaded')
	time.sleep(1.5)

GPIO.setmode(GPIO.BOARD)

global ControlPin
ControlPin = {'x':[29,31,33,35],
		'y':[37,36,38,40]}

for pin in ControlPin['x']:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)
for pin in ControlPin['y']:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)

GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

global x_lim
global y_lim
x_lim = float(180)
y_lim = float(180)

def checklimit(axis):
	global x_lim
	global y_lim
	if axis == 'x':
		if x_lim >= 360 or x_lim <= 0:
			return True
	if axis == 'y':
		if y_lim >= 300 or y_lim <= 60:
			return True
	return False

def updatelim(dir,axis):
	global x_lim
	global y_lim
	if dir == 1:
		x = 1
	if dir == 0:
		x = -1
	if axis == 'x':
		x_lim = x_lim + (.703125 * x)
	if axis == 'y':
		y_lim = y_lim + (.703125 * x)

def go(seq,steps,speed,axis):
	global x_lim
	global y_lim
	for i in range(steps):
		updatelim(seq[1][1],axis)
		if checklimit(axis) == True:
			break
		for halfstep in range(8):
			for pin in ControlPin[axis]:
				GPIO.output(pin, seq[halfstep][ControlPin[axis].index(pin)])
			time.sleep(float(speed)/1000)

def home(axis):
	global x_lim
	global y_lim
	if axis == 'x':
		while x_lim <> 180:
			if x_lim > 180:
				go(b,1,2,axis)
			if x_lim < 180:
				go(f,1,2,axis)	
	if axis == 'y':
		while y_lim <> 180:
			if y_lim > 180:
				go(b,1,2,axis)
			if y_lim < 180:
				go(f,1,2,axis)


f = [ [1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1] ]

b = [ [0,0,0,1],
	[0,0,1,1],
	[0,0,1,0],
	[0,1,1,0],
	[0,1,0,0],
	[1,1,0,0],
	[1,0,0,0],
	[1,0,0,1] ]

log = False

try:

	char=''
	os.system('clear')
	print 'Press x to exit'
	while char != 'x' :
		if log:
			workfile.write(logstep)
			if timeoff > 0:
				workfile.write("time.sleep(" + str(timeoff) + ")\n")
			logstep = ''

		timeoff = 0
		starttime = int(round(time.time()))
		char = readchar.readchar()
		timeoff = int(round(time.time())) - starttime
		print('Pressed ' + char + ' after ' + str(timeoff) + ' seconds.') 
		if char == 'w':
			go(b,3,2,'y')
			if log:
				logstep = "go(b,3,2,'y')\n"
		elif char == 's':
			go(f,3,2,'y')
			if log:
				logstep = "go(f,3,2,'y')\n"
		elif char == 'a':
			go(b,3,2,'x')
			if log:
				logstep = "go(b,3,2,'x')\n"
		elif char == 'd':
			go(f,3,2,'x')	
			if log:
				logstep = "go(f,3,2,'x')\n"
		elif char == 'r' and log != True:
			os.system('clear')
			print('Recording')
			log = True
			logstep = ''
			workfile = open('recording.py', 'w')
			#workfile.write('def run():\n')
		elif char == 'p' and len(argv) > 1:
			print('Playback Started')
			execfile(routine)
			print('Playback Complete')

except KeyboardInterrupt():
	raise ValueError('...Ctrl + C Presses. Exiting Now')
finally:
	if log:
		workfile.close()
	home('x')
	home('y')
	GPIO.cleanup()
	os.system('kill -9 $PPID')

import RPi.GPIO as GPIO
import time
import tty
import sys
import os
from sys import argv

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

try:

	tty.setraw(sys.stdin.fileno())
	char=''
	os.system('clear')
	print 'Press x to exit'
	while char != 'x' :
		char = sys.stdin.read(1)
		if char == 'w':
			go(b,3,2,'y')
		if char == 's':
			go(f,3,2,'y')
		if char == 'a':
			go(b,3,2,'x')
		if char == 'd':
			go(f,3,2,'x')	


except KeyboardInterrupt():
	raise ValueError('...Ctrl + C Presses. Exiting Now')
finally:
	home('x')
	home('y')
	GPIO.cleanup()
	os.system('kill -9 $PPID')

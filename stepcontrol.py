import RPi.GPIO as GPIO
import time
import readchar
import sys
import os
from sys import argv

#Comments Comments Comments

if len(argv)> 1: #if an argument is used while executing from the command line
	routine = argv[1] #use that for the routine/playback file
	print('Routine loaded as: ' + routine)
	time.sleep(1.5)
else:
	print('No routine loaded')
	time.sleep(1.5)

GPIO.setmode(GPIO.BOARD) #Set Raspberry Pi GPIO to BOARD numbering (as opposed to BCM)

ControlPin = {'x':[29,31,33,35],
		'y':[37,36,38,40]}

for pin in ControlPin['x']:
	GPIO.setup(pin, GPIO.OUT) #Set each pin to the OUTPUT mode
	GPIO.output(pin,0) #Make sure they start as Off
for pin in ControlPin['y']:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)

GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #Keeping this for when I add sensors / limit switches, useless for now

x_lim = float(180) #using type float() so we don't lose degrees over time from rounding
y_lim = float(180)

def checklimit(axis): #Returns true or false during go() to signal that the global limits are within/outside their set range
	if axis == 'x':
		return x_lim >= 360 or x_lim <= 0
	else:
		return y_lim >= 300 or y_lim <= 60

def updatelim(dir,axis): #update current angle of global limit vars based on current vector
	global x_lim
	global y_lim
	if dir == 1: #first number of sequence handed to updatelim is either 1 or 0 (forward or backwards) this determins direciton of vector
		x = 1
	if dir == 0:
		x = -1
	if axis == 'x':
		x_lim = x_lim + (.703125 * x) #these motors have 512 steps per revolution, each step is .703125 degrees
	if axis == 'y':
		y_lim = y_lim + (.703125 * x)

def go(seq,steps,speed,axis): #Takes the forward or backwards sequence, number of steps, delay between steps in microseconds, and axis to move the appropriate motors the desired number of steps 
	global x_lim
	global y_lim
	for i in range(steps): #in a typical keypress, this is 1 
		updatelim(seq[1][1],axis) #checks the first number of the current sequence to determine whether this is forward or backwards (see updatelim)
		if checklimit(axis) == True: #If the axis is outside it's limits, nope nope nope nope.
			break 
		for halfstep in range(8): #the sequences of 1's and 0's later on (f/b sequences) represent the on/off state of each output pin for a given axis. we have to switch this 8 times just to do one step
			for pin in ControlPin[axis]: #for each one of THOSE 8 sequences, we change the four output pins accordingly
				GPIO.output(pin, seq[halfstep][ControlPin[axis].index(pin)])
			time.sleep(float(speed)/1000) #we're moving a physical metal shaft here, so let's sleep and let it have a bit of time to catch up to what we're outputting, or else the motor will skip steps and not move anywhere.

def home(axis):
	global x_lim
	global y_lim
	if axis == 'x': #pretty simple. Monitor x and y axis angles until each is at 180 (striaght up).
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


f = [ [1,0,0,0], #each group in this sequence represents the state of four output pins.
	[1,1,0,0], #imagine the diagonal shape of 1's as the direction we're pushing magnetic current
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

keymap = {'w':[b,1,2,'y'], #Created a dictionary of all key mappings, and direciton/steps/speed/axis for each key.
	  's':[f,1,2,'y'], #I've created more keys for a "two handed layout" to make moving the gimal in either 1 small step, or one step of 45 degrees.
	  'a':[b,1,2,'x'],
	  'd':[f,1,2,'x'],
	  'i':[b,64,2,'y'],
	  'k':[f,64,2,'y'],
	  'j':[b,64,2,'x'],
	  'l':[f,64,2,'x']}

keylog = {'w':"go(b,1,2,'y')\n", #These are the strings put into a recording file.
	  's':"go(f,1,2,'y')\n",
	  'a':"go(b,1,2,'x')\n",
	  'd':"go(f,1,2,'x')\n",
	  'i':"go(b,64,2,'y')\n",
	  'k':"go(f,64,2,'y')\n",
	  'j':"go(b,64,2,'x')\n",
	  'l':"go(f,64,2,'x')\n",
	  'h':"home('x')\nhome('y')"}

try: #The Action

	char='' #declare as string
	os.system('clear') #clear the screen
	print 'Press x to exit' #basic instruction :)
	while char != 'x' : #I don't need explain this much.

		timeoff = 0
		starttime = int(round(time.time())) #Get System time
		char = readchar.readchar() #wait for character
		timeoff = int(round(time.time())) - starttime #how long did that take? (used for log)
		os.system('clear') #Clear the screen
		print('Pressed ' + char + ' after ' + str(timeoff) + ' seconds.')
#Main
		if char in keymap: #grab the appropriate settings for each keypress that exists in our Keymap Dictionary, and work magic in the go() function
			go(*keymap[char])

		if log: #If we're recording, let's log what we just did from a pre compiled list of strings, Keylog.
			if char in keylog:
				workfile.write(keylog[char])
				if timeoff > 2: #Ignore keypress delays that took less than two seconds. change as needed
					workfile.write("time.sleep(" + str(timeoff) + ")\n")

		elif char == 'r' and not log: #Start recording. Open working file. (overwrite it each time)
			os.system('clear')
			print('Recording')
			log = True
			workfile = open('recording.txt', 'w')
		elif char == 'h': 
			home('x')
			home('y')
		elif char == 'p' and len(argv) > 1: #If we loaded a file, we will execute it using the sketchy execfile() function
			print('Playback Started')
			execfile(routine)
			print('Playback Complete')

except KeyboardInterrupt(): #I'm still new at this...
	raise ValueError('...Ctrl + C Presses. Exiting Now')
finally:
	if log: #If we opened a file, lets save and close it, then rename it within the system
		workfile.close()
		os.system('clear')
		fname = raw_input('Please name your recording: ')
		os.system('mv recording.txt ' + str(fname) + '.txt')
		print('file saved as ' + str(fname) + '.txt') 
	home('x')
	home('y') #Home 'yo
	GPIO.cleanup() #Set the GPIO pins back to their normal state. pretty much required.

import time
import math
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
in_pin = 21 #chage that
gpio.setup(in_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

outputs = [17, 27, 22, 23, 24, 25, 19, 26, 16, 20] #list of output pins
for i in outputs:
	gpio.setup(i,gpio.OUT, initial = 1)

pwms = [gpio.PWM(pin, 500) for pin in outputs]
for thing in pwms:
	thing.start(0)


def brightness(t, phase):
	f = 0.2
	B = (math.sin(2*math.pi*f*t - phase))**2
	return B*100

def set_brights(t):
	phi = math.pi/11
	for n, thing in enumerate(pwms):
		thing.ChangeDutyCycle(brightness(t, phi*n))

flip = 1 #forward
time_ref = 0
fake_time = 0
delta_time = 0
i_hate_this = 0
start_time = time.time()
def flipflop(channel):
	#global time_ref
	#global i_hate_this
	#time_ref = fake_time
	global flip
	if flip==-1:
		flip = 1 #go forwards
	else:
		flip = -1 #go backwards
		#i_hate_this = delta_time #i love placeholder variables

def do_shit(flop):
	global fake_time
	delta_time = time.time() - i_hate_this#-start_time - i_hate_this
	i_hate_this = time.time()
	fake_time += flip*delta_time
	set_brights(fake_time)
	print(fake_time)

gpio.add_event_detect(in_pin, gpio.RISING, callback = flipflop, bouncetime = 500)

try:
	while 1:
		do_shit(flip)
except KeyboardInterrupt:
	gpio.cleanup()
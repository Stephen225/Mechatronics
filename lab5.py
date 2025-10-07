import time
import math
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
in_pin = 21 #chage that
gpio.setup(in_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

outputs = [17, 27, 22, 23, 24, 25, 19, 26, 16, 20] #in order of led wiring
for i in outputs:
	gpio.setup(i,gpio.OUT, initial = 1)

pwms = [gpio.PWM(pin, 500) for pin in outputs] #initialize all the pwm pins
for thing in pwms:
	thing.start(0)


def brightness(t, phase):
	f = 0.2
	B = (math.sin(2*math.pi*f*t - phase))**2 #math rahhh
	return B*100

def set_brights(t):
	phi = math.pi/11
	for n, thing in enumerate(pwms): #enumerate rahhhhh
		thing.ChangeDutyCycle(brightness(t, phi*n))

flip = 1 #forward
fake_time = 0 #modified time to fold over itself
delta_time = 0 
i_hate_this = 0
def flipflop(channel): #changes direction 
	global flip
	if flip==-1:
		flip = 1 #go forwards
	else:
		flip = -1 #go backwards

def do_shit(flop):
	global fake_time
	global i_hate_this
	delta_time = time.time() - i_hate_this #get delta from last timestep
	i_hate_this = time.time() #reset delta reference for next go
	fake_time += flip*delta_time #either add or subtract delta based on flip
	set_brights(fake_time) #go go gadget flashlight

gpio.add_event_detect(in_pin, gpio.RISING, callback = flipflop, bouncetime = 100)

try:
	while 1:
		do_shit(flip)
except KeyboardInterrupt:
	gpio.cleanup()
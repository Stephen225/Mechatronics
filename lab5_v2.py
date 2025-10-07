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

for i in pwms:
	i.start(0)

def brightness (t, phase):
	f = 0.2
	B = (math.sin(2*math.pi*f*t - phase))**2
	return B*100

def set_brights(t):
	phi = math.pi/11
	for i, thing in enumerate(pwms):
		thing.ChangeDutyCycle(brightness(t, phi*i))

flip = 0
time_ref = 0
fake_time = 0
start_time = time.time()
def flipflop(channel):
	global time_ref
	close = fake_time%(2*math.pi)
	time_ref += 2*(2*math.pi-close)

def do_shit(flop):
	global fake_time
	fake_time = time_ref + time.time() - start_time
	set_brights(fake_time)
	print(fake_time)

gpio.add_event_detect(in_pin, gpio.RISING, callback = flipflop, bouncetime = 100)

try:
	while 1:
		do_shit(flip)
except KeyboardInterrupt:
	gpio.cleanup()
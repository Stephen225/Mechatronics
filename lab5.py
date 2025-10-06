import time
import math
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
in_pin = 21 #chage that
gpio.setup(in_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

outputs = [17, 27, 22, 23, 24, 25, 19, 26, 16, 20] #list of output pins
for i in outputs:
	gpio.setup(i,gpio.OUT, initial = 1)
pwm1 = gpio.PWM(outputs[0], 500) #change this to make all the pwms
pwm2 = gpio.PWM(outputs[1], 500) #change this to make all the pwms
pwm3 = gpio.PWM(outputs[2], 500) #change this to make all the pwms
pwm4 = gpio.PWM(outputs[3], 500) #change this to make all the pwms
pwm5 = gpio.PWM(outputs[4], 500) #change this to make all the pwms
pwm6 = gpio.PWM(outputs[5], 500) #change this to make all the pwms
pwm7 = gpio.PWM(outputs[6], 500) #change this to make all the pwms
pwm8 = gpio.PWM(outputs[7], 500) #change this to make all the pwms
pwm9 = gpio.PWM(outputs[8], 500) #change this to make all the pwms
pwm10 = gpio.PWM(outputs[9], 500) #change this to make all the pwms

def brightness (t, phase):
	f = 0.2
	B = (math.sin(2*math.pi()*f*t - phase))^2
	return B

def set_brights(t):
	phi = math.pi()/11
	pwm1.ChangeDutyCycle(brightness(t, phi*0)) #may have to hardcode
	pwm2.ChangeDutyCycle(brightness(t, phi*1)) #may have to hardcode
	pwm3.ChangeDutyCycle(brightness(t, phi*2)) #may have to hardcode
	pwm4.ChangeDutyCycle(brightness(t, phi*3)) #may have to hardcode
	pwm5.ChangeDutyCycle(brightness(t, phi*4)) #may have to hardcode
	pwm6.ChangeDutyCycle(brightness(t, phi*5)) #may have to hardcode
	pwm7.ChangeDutyCycle(brightness(t, phi*6)) #may have to hardcode
	pwm8.ChangeDutyCycle(brightness(t, phi*7)) #may have to hardcode
	pwm9.ChangeDutyCycle(brightness(t, phi*8)) #may have to hardcode
	pwm10.ChangeDutyCycle(brightness(t, phi*9)) #may have to hardcode

flip = True
time_ref = 0
time = 0
def flipflop():
	time_ref = time
	if flip:
		flip = False
	else:
		flip = True

def do_shit(flop):
	if flip:
		time = time_ref - time.time()
	else:
		time = time_ref + time.time()
	set_brights(time)

gpio.add_event_detect(in_pin, gpio.RISING, callback = flipflop(), bounce_time = 1)

try:
	while 1:
		do_shit(flip)
except:
	gpio.cleanup()
from shifter import Shifter, Bug
import RPi.GPIO as GPIO
import time
import random as rand

serialPin, latchPin, clockPin = 23, 24, 25
go, wrap, fast = 16, 20, 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial = 0)
GPIO.setup(clockPin, GPIO.OUT, initial = 0)

gpio.setup(go, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(wrap, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(fast, gpio.IN, pull_up_down = gpio.PUD_DOWN)

boog = Bug()

doIGo = True
def bugGo():
	global doIGo
	if doIGo:
		boog.start()
	else:
		boog.stop()

def bugNoGO():
	boog.stop()

doIWrap = True
def wrapFlip():
	global doIWrap
	boog.isWrapOn = doIWrap
	doIWrap = not doIWrap

#bugSpeed = 0.1
def fastOn():
	boog.timestep = 0.1/3

def fastOff():
	boog.timestep = 0.1


gpio.add_event_detect(go, gpio.RISING, callback = bugGO, bouncetime = 50)
gpio.add_event_detect(wrap, gpio.RISING, callback = wrapFlip, bouncetime = 50)
gpio.add_event_detect(fast, gpio.RISING, callback = fastOn, bouncetime = 50)
gpio.add_event_detect(fast, gpio.FALLING, callback = fastOff, bouncetime = 50)



#boog.start()

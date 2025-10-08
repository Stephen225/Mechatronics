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

GPIO.setup(go, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(wrap, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(fast, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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


GPIO.add_event_detect(go, GPIO.RISING, callback = bugGo, bouncetime = 50)
GPIO.add_event_detect(wrap, GPIO.RISING, callback = wrapFlip, bouncetime = 50)
GPIO.add_event_detect(fast, GPIO.RISING, callback = fastOn, bouncetime = 50)
GPIO.add_event_detect(fast, GPIO.FALLING, callback = fastOff, bouncetime = 50)



#boog.start()

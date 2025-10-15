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

boog = Bug(0.1,3,False,1) #extra call here bc i added more bugs, see the shifter code

doIGo = True
def bugGo(channel):
	global doIGo
	if doIGo:
		boog.start()
		doIGo = not doIGo
	else:
		boog.stop()
		doIGo = not doIGo

def bugNoGO(channel):
	boog.stop()

doIWrap = True
def wrapFlip(channel):
	global doIWrap
	boog.isWrapOn = doIWrap
	doIWrap = not doIWrap

bugSpeed = 0.1
doIFast = False
def fastOn(channel):
	global doIFast
	if doIFast:
		boog.timestep = bugSpeed/3
		doIFast = not doIFast
	else:
		boog.timestep = bugSpeed
		doIFast = not doIFast

def fastOff(channel):
	boog.timestep = 0.1


GPIO.add_event_detect(go, GPIO.RISING, callback = bugGo, bouncetime = 50)
GPIO.add_event_detect(wrap, GPIO.RISING, callback = wrapFlip, bouncetime = 50)
GPIO.add_event_detect(fast, GPIO.RISING, callback = fastOn, bouncetime = 50)
#GPIO.add_event_detect(fast, GPIO.FALLING, callback = fastOff, bouncetime = 50)


try:
	while 1:
		boog.doBugStuff()
except KeyboardInterrupt:
	GPIO.cleanup()
#boog.start()

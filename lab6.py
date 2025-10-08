from shifter import Shifter
import time
import RPi.GPIO as GPIO

serialPin, latchPin, clockPin = 23, 24, 25

shifter = Shifter(serialPin, latchPin, clockPin)

try:
	while 1:
		print("go")
		shifter.shiftByte(0b10101010)
		print("done")
except:
	GPIO.cleanup()
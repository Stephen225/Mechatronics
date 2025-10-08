import Shifter
import time
import RPi.GPIO as GPIO

serialPin, latchPin, clockPin = 23, 24, 25

shifter = Shifter(serialPin, latchPin, clockPin)

try:
	while 1:
		shifter.shiftByte(0b10101010)
except:
	GPIO.cleanup()
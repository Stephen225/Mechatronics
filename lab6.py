from shifter import Shifter
import time
import RPi.GPIO as GPIO
import random as rand

serialPin, latchPin, clockPin = 23, 24, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial = 0)
GPIO.setup(clockPin, GPIO.OUT, initial = 0)

shifter = Shifter(serialPin, latchPin, clockPin)

bugs = [2**i for i in range(8)]
bugIndex = rand.randint(0,7)

try:
	while 1:
		shifter.shiftByte(bugs[bugIndex])
		time.sleep(0.05)
		if rand.randint(0,1) == 1:
			bugIndex += 1
			if bugIndex == 8: bugIndex = 6
		else:
			bugIndex -= 1
			if bugIndex == -1: bugIndex = 2
except KeyboardInterrupt:
	GPIO.cleanup()
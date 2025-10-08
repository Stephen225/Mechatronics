from shifter import Shifter
import time
import RPi.GPIO as GPIO

serialPin, latchPin, clockPin = 23, 24, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial = 0)
GPIO.setup(clockPin, GPIO.OUT, initial = 0)

shifter = Shifter(serialPin, latchPin, clockPin)

try:
	while 1:
		print("go")
		shifter.shiftByte(0b10101010)
		time.sleep(0.5)
		shifter.shiftByte(0b01010101)
		time.sleep(0.5)
except:
	GPIO.cleanup()
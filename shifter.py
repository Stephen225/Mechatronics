import RPi.GPIO as GPIO
import time

class Shifter:
	def __init__(self, a, b, c):
		self.serialPin, self.latchPin, self.clockPin = a, b, c

	def __ping(self, pin):
		GPIO.output(pin, 1)
		time.sleep(0)
		GPIO.output(pin, 0)

	def shiftByte(self, byte):
		for i in range(8):
			GPIO.output(self.serialPin, byte & (1<<i))
			__ping(self.clockPin)
			print(byte & (1<<i))
		__ping(self.latchPin)
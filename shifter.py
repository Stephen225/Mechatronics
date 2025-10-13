import RPi.GPIO as GPIO
import time
import random as rand

class Shifter:
	def __init__(self, a=23, b=24, c=25):
		self.serialPin, self.latchPin, self.clockPin = a, b, c

	def __ping(self, pin):
		GPIO.output(pin, 1)
		time.sleep(0)
		GPIO.output(pin, 0)

	def shiftByte(self, byte):
		for i in range(8):
			GPIO.output(self.serialPin, byte & (1<<i))
			self.__ping(self.clockPin)
		self.__ping(self.latchPin)

class Bug:
	def __init__(self, timestep = 0.1, x = 3, isWrapOn = False):
		self.timestep, self.x, self.isWrapOn = timestep, x, isWrapOn
		self.__shifter = Shifter()
		self.bugs = [2**i for i in range(8)]
		self.bugIndex = rand.randint(0,7)
		self.go = False


	def start(self):
		self.go = True

	def stop(self):
		self.go = False

	def doBugStuff(self):
		if self.go:
				self.__shifter.shiftByte(self.bugs[self.bugIndex])
				time.sleep(self.timestep)
				if rand.randint(0,1) == 1:
					self.bugIndex += 1
					if self.bugIndex == 8: 
						if not self.isWrapOn:
							self.bugIndex = 6
						else:
							self.bugIndex = 0
				else:
					self.bugIndex -= 1
					if self.bugIndex == -1: 
						if not self.isWrapOn:
							self.bugIndex = 2
						else:
							self.bugIndex = 7


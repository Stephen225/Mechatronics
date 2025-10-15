import RPi.GPIO as GPIO
import time
import random as rand

#sorry for resubmitting, i forgot to make the stop command turn off the LED

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
	def __init__(self, timestep = 0.1, x = 3, isWrapOn = False, bugs = 1):
		self.timestep, self.x, self.isWrapOn = timestep, x, isWrapOn
		self.__shifter = Shifter()
		self.bugs = [2**i for i in range(8)]
		self.numBugs = bugs
		self.bugIndex = [rand.randint(0,7) for i in range(self.numBugs)]
		self.go = False

		#also i decided to add in the capability to add more bugs
		#bc who doesnt want more than one bug

	def start(self):
		self.go = True

	def stop(self):
		self.go = False
		self.__shifter.shiftByte(0)

	def doBugStuff(self):
		if self.go:
				pattern = 2**8-1
				for thing in set(self.bugs[self.bugIndex[i]] for i in range(len(self.bugIndex))):
					#this gets the set of unique bug index values (bugs can occupy the same space)
					#and then you just add them together and that gives the bug positions
					pattern -= thing
				self.__shiftr.shiftByte(pattern)
				time.sleep(self.timestep)
				for i in range(len(self.bugIndex)):
					if rand.randint(0,1) == 1:
						self.bugIndex[i] += 1
						if self.bugIndex[i] == 8: 
							if not self.isWrapOn:
								self.bugIndex[i] = 6
							else:
								self.bugIndex[i] = 0
					else:
						self.bugIndex[i] -= 1
						if self.bugIndex[i] == -1: 
							if not self.isWrapOn:
								self.bugIndex[i] = 2
							else:
								self.bugIndex[i] = 7


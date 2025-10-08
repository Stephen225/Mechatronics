import RPi.GPIO as GPIO
import time

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


	def start(self):
		try:
			while 1:
				self.__shifter.shiftByte(bugs[bugIndex])
				time.sleep(0.05)
				if rand.randint(0,1) == 1:
					self.bugIndex += 1
					if self.bugIndex == 8: self.bugIndex = 6
				else:
					self.bugIndex -= 1
					if self.bugIndex == -1: self.bugIndex = 2
		except KeyboardInterrupt:
			GPIO.cleanup()
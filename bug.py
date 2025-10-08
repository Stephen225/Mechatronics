from shifter import Shifter, Bug
import RPi.GPIO as GPIO
import time
import random as rand

serialPin, latchPin, clockPin = 23, 24, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial = 0)
GPIO.setup(clockPin, GPIO.OUT, initial = 0)

boog = Bug()
boog.start()
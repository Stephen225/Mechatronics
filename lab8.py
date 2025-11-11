# stepper_class_shiftregister_multiprocessing.py
#
# Stepper class
#
# Because only one motor action is allowed at a time, multithreading could be
# used instead of multiprocessing. However, the GIL makes the motor process run 
# too slowly on the Pi Zero, so multiprocessing is needed.

import time
import multiprocessing
from shifter import Shifter   # our custom Shifter class

class Stepper:
    """
    Supports operation of an arbitrary number of stepper motors using
    one or more shift registers.
  
    A class attribute (shifter_outputs) keeps track of all
    shift register output values for all motors.  In addition to
    simplifying sequential control of multiple motors, this schema also
    makes simultaneous operation of multiple motors possible.
   
    Motor instantiation sequence is inverted from the shift register outputs.
    For example, in the case of 2 motors, the 2nd motor must be connected
    with the first set of shift register outputs (Qa-Qd), and the 1st motor
    with the second set of outputs (Qe-Qh). This is because the MSB of
    the register is associated with Qa, and the LSB with Qh (look at the code
    to see why this makes sense).
 
    An instance attribute (shifter_bit_start) tracks the bit position
    in the shift register where the 4 control bits for each motor
    begin.
    """

    # Class attributes:
    num_steppers = 0      # track number of Steppers instantiated
    shifter_outputs = 0   # track shift register outputs for all motors
    seq = [0b0001,0b0011,0b0010,0b0110,0b0100,0b1100,0b1000,0b1001] # CCW sequence
    #seq = [0b0001, 0b0010, 0b0100, 0b1000]
    delay = 2000          # delay between motor steps [us]
    steps_per_degree = 4096/360    # 4096 steps/rev * 1/360 rev/deg

    def __init__(self, shifter, lock, angle):
        self.s = shifter           # shift register
        self.angle = angle            # current output shaft angle
        self.step_state = 0        # track position in sequence
        self.shifter_bit_start = 4*Stepper.num_steppers  # starting bit position
        self.lock = lock           # multiprocessing lock

        Stepper.num_steppers += 1   # increment the instance count

    # Signum function:
    def __sgn(self, x):
        if x == 0: return(0)
        else: return(int(abs(x)/x))

    # Move a single +/-1 step in the motor sequence:
    def __step(self, direc):
        #with self.lock:
        #print("pre direc state ",self.step_state,flush=True)
        self.step_state += direc   # increment/decrement the step
        #print("post direc state ",self.step_state,flush=True)
        self.step_state %= 8      # ensure result stays in [0,7]
        #print("post mod state ",self.step_state,flush=True)
        #Stepper.shifter_outputs |= 0b1111<<self.shifter_bit_start
        #Stepper.shifter_outputs &= Stepper.seq[self.step_state]<<self.shifter_bit_start
        Stepper.shifter_outputs &= ~(0b1111<<self.shifter_bit_start)
        Stepper.shifter_outputs |= Stepper.seq[self.step_state]<<self.shifter_bit_start
        #print("post bitwise state ",self.step_state,flush=True)
        #print(str(self.shifter_bit_start)+" "+str(Stepper.shifter_outputs))
        #print(bin(Stepper.shifter_outputs.value))
        #print(self.shifter_bit_start," ",self.step_state, flush=True)
        #print(f"[Motor {self.shifter_bit_start}] step_state={self.step_state} angle={self.angle:.2f}", flush=True)
        self.s.shiftByte(Stepper.shifter_outputs)
        #print("post shift state ",self.step_state,flush=True)
        self.angle += direc/Stepper.steps_per_degree
        self.angle %= 360         # limit to [0,359.9+] range
        #print("post angle state ",self.step_state,flush=True)

    # Move relative angle from current position:
    def __rotate(self, delta):
        self.lock.acquire()                 # wait until the lock is available
        numSteps = int(Stepper.steps_per_degree * abs(delta))    # find the right # of steps
        direc = self.__sgn(delta)        # find the direction (+/-1)
        #print(f"going {numSteps} steps in {direc} direction", flush=True)
        for i in range(numSteps):      # take the steps
            #print(f"step {i} going {direc}")
            #self.lock.acquire()
            #print("step on shifta ",self.shifter_bit_start,flush=True)
            #print("step start state ",self.step_state,flush=True)   
            self.__step(direc)
            #print("step end state ",self.step_state,flush=True)
            #self.lock.release()
            time.sleep(Stepper.delay/1e6)
        self.lock.release()

    # Move relative angle from current position:
    def rotate(self, delta):
        time.sleep(0.1)
        p = multiprocessing.Process(target=self.__rotate, args=(delta,))
        p.start()
        p.join()

    # Move to an absolute angle taking the shortest possible path:
    def goAngle(self, angle):
        self.delta = angle-self.angle
        self.rotate(self.delta)
         # COMPLETE THIS METHOD FOR LAB 8

    # Set the motor zero point
    def zero(self):
        self.angle = 0


# Example use:

if __name__ == '__main__':

    fuck = 0b00010000
    fuck &= ~(0b1111<<0)
    fuck |= 0b0001<<0
    print(fuck)
    fuck &= ~(0b1111<<4)
    fuck |= 0b0011<<4
    print(fuck)


    s = Shifter(data=16,latch=20,clock=21)   # set up Shifter

    # Use multiprocessing.Lock() to prevent motors from trying to 
    # execute multiple operations at the same time:
    lock1 = multiprocessing.Lock()
    lock2 = multiprocessing.Lock()

    angle1 = multiprocessing.Value('f')
    angle2 = multiprocessing.Value('f')
    #Stepper.shifter_outputs = multiprocessing.Value('i',0)

    # Instantiate 2 Steppers:
    m1 = Stepper(s, lock1, angle1)
    m2 = Stepper(s, lock2, angle2)

    # Zero the motors:
    m1.zero()
    m2.zero()

    # Move as desired, with eacg step occuring as soon as the previous 
    # step ends:
    m1.rotate(-90)
    m1.rotate(45)
    m1.rotate(-90)
    m1.rotate(45)

    # If separate multiprocessing.lock objects are used, the second motor
    # will run in parallel with the first motor:
    m2.rotate(180)
    m2.rotate(-45)
    m2.rotate(45)
    m2.rotate(-90)
 
    # While the motors are running in their separate processes, the main
    # code can continue doing its thing: 
    try:
        while True:
            pass
    except:
        print('\nend')
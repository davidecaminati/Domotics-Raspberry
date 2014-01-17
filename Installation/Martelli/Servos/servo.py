#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device with i2c adress
pwm = PWM(0x44, debug=True)
#this is the max/min value for servo TOWER PRO MG995
#MIN_VAL0 = 200
#MAX_VAL0 = 680
#MIN_VAL4 = 220
#MAX_VAL4 = 700

STEP_SLOWER = 0.02
servoMin = 220  # Min pulse length out of 4096
servoMax = 420  # Max pulse length out of 4096


pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def Open(servonum):
  for i in range(servoMin,servoMax):
    pwm.setPWM(servonum, 0, i)
    time.sleep(STEP_SLOWER)
  return "ok"
  
def Close(servonum):
  for i in range(servoMax-servoMin):
    pwm.setPWM(servonum, 0,servoMax - i)
    time.sleep(STEP_SLOWER)
  return "ok"
  
  
Open(0)
time.sleep(3)
Close(0)
Open(4)
time.sleep(3)
Close(4)
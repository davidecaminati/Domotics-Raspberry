#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x44, debug=True)

#servoMin = 150  # Min pulse length out of 4096
servoMin = 200  # Min pulse length out of 4096
#servoMax = 600  # Max pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  #pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength = 100                   # 1,000,000 us per second
  pulseLength /= 2                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)
  print "setServoPulse"
  
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  for i in range(servoMin,servoMax):
    pwm.setPWM(0, 0, i)
  time.sleep(1)
  for i in range(servoMax-servoMin):
    pwm.setPWM(0, 0,servoMax- i)
  time.sleep(1)
  #print "servoMin", servoMin
  #time.sleep(1)
  #pwm.setPWM(0, 0, servoMid)
  #print "servoMid", servoMid
  #time.sleep(1)
  #pwm.setPWM(0, 0, servoMax)
  #print "servoMax", servoMax
  #time.sleep(1)
  #pwm.setPWM(0, 0, servoMid)
  #print "servoMid", servoMid
  #time.sleep(1)
  #print "-----"




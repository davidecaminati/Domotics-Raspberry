#!/usr/bin/env python
import subprocess
import RPi.GPIO as GPIO

channel=24
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(channel, GPIO.FALLING)

subprocess.call(['/sbin/reboot'])
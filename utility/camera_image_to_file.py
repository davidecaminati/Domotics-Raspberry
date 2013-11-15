#!/usr/bin/python
import pygame, sys
from pygame.locals import *
import pygame.camera
import time

pygame.init()
pygame.camera.init()
L = []
L = [352,288,640,480]
count = 0
while count < 4:
   width = L[count]
   height = L[count+1]
   cam = pygame.camera.Camera("/dev/video0",(width,height))
   cam.start()
   pygame.display.set_caption(str(width) + "x" + str(height) + "  saved as /home/pi/" + str(width) + "x" + str(height) + '.jpg')
   windowSurfaceObj = pygame.display.set_mode((width,height))
   image = cam.get_image()
   catSurfaceObj = image
   windowSurfaceObj.blit(catSurfaceObj,(0,0))
   pygame.display.update()
   cam.stop()
   pygame.image.save(image,str(width) + "x" + str(height) +'.jpg')
   count +=2
   time.sleep(2)

import sys, pygame,time
import smbus
import time
import urllib
import urllib2
import spidev
from Adafruit_PWM_Servo_Driver import PWM
#SERVO#
# Initialise the PWM device with i2c adress
pwm = PWM(0x44, debug=True)


pwm.setPWMFreq(60) # Set frequency to 60 Hz
#END SERVO#
  
#settings for MCP 23017#
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
DEVICE = 0x24 # DEVICE address (A0-A2)
IODIRA = 0x00 # Pin direction register for port A (right)
IODIRB = 0x01 # Pin direction register for port B (left)
OLATA  = 0x14 # Register for outputs for port A
OLATB  = 0x15 # Register for outputs for port B
GPIOA  = 0x12 # Register for inputs for port A
GPIOB  = 0x13 # Register for inputs for port B
GPPUA  = 0x0C # Pull-up resistor (0 = disabled, 1 = enabled)
GPPUB  = 0x0D # Pull-up resistor (0 = disabled, 1 = enabled)

OldState = 255
bus.write_byte_data(DEVICE,GPPUB,0xff) # Set PullUp resistor for input register
#end setting for MCP 23017#
bus.write_byte_data(DEVICE,IODIRA,0x00) # all A output
bus.write_byte_data(DEVICE,GPPUA,0xff) # all A pull up

#
bus.write_byte_data(DEVICE,OLATA,0x00) # all A rele ON
bus.read_byte_data(DEVICE,GPIOA) #read status A 
bus.write_byte_data(DEVICE,OLATA,0xff) # all A rele off
#

#GAS and TEMP
GAS_CLEAN_AIR = 377
spi = spidev.SpiDev()
spi.open(0, 0)

#Url for change state of reles
urlForToggle = 'http://192.168.0.202:5000/reletoggle/'
#Url for read state of rele
urlForState = 'http://192.168.0.202:5000/relestate/'
#Url for dimm on
urlForDimmOn = 'http://192.168.0.202:5000/reledimmon/'
#Url for dimm off
urlForDimmOff = 'http://192.168.0.202:5000/reledimmoff/'

pygame.init()
size = width, height = 480, 234
screen = pygame.display.set_mode((size),pygame.FULLSCREEN)
clock = pygame.time.Clock()

done = False
font = pygame.font.SysFont("comicsansms", 42)
pygame.mouse.set_visible(False)

class Servo(object):
    def __init__(self, name, servoMin, servoMax, servonum):
        self.name = name
        self.servoMin = servoMin
        self.servoMax = servoMax
        self.servonum = servonum
        self.step_slower = 0.002
        self.state = ""
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Servo: %s>" % self
                
    def Open(self):
      for i in range(self.servoMin,self.servoMax):
        pwm.setPWM(self.servonum, 0, i)
        time.sleep(self.step_slower)
        self.state = "Open"
        
    def Close(self):
      for i in range(self.servoMax-self.servoMin):
        pwm.setPWM(self.servonum, 0,self.servoMax - i)
        time.sleep(self.step_slower)
        self.state = "Close"
             
    def State(self):
        return self.state
        
    def Text(self):
        text = font.render(str(self.name) + " " + str(self.state), True, (128, 128, 0))
        return text
        
class TemperatureProbe(object):
    def __init__(self, name,adcnum ):
        self.name = name
        self.adcnum = adcnum
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<TemperatureProbe: %s>" % self
        
    def readadc(self):
            # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        if self.adcnum > 7 or self.adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + self.adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        #debug in some case, strange, but after read the pullup resistor register fail, need to be re set
        #bus.write_byte_data(DEVICE,GPPUB,0xff) # Set PullUp resistor for input register
        #debug
        val = (adcout - 780 )/10
        return val
        
    def Text(self):
        text = font.render(str(self.name) + " " + str(self.readadc()), True, (0, 128, 128))
        return text
  
class Rele(object):
    def __init__(self, name, relenum):
        self.name = name
        self.relenum = relenum
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Home: %s>" % self
           
    def Read_state(self):
        OldState = bus.read_byte_data(DEVICE,GPIOA)
        BinReleNumber = 2** (self.relenum - 1)
        if BinReleNumber & OldState == BinReleNumber:
            return "off"
        else:
            return "on"
            
    def On(self):
        OldState = bus.read_byte_data(DEVICE,GPIOA)
        BinReleNumber = 2** (self.relenum - 1)
        if BinReleNumber & OldState == BinReleNumber:
            NewValue = OldState - BinReleNumber
            bus.write_byte_data(DEVICE,OLATA,NewValue)
            return "ok"
        else:
            return "already done"
            
    def Off(self):
        OldState = bus.read_byte_data(DEVICE,GPIOA)
        BinReleNumber = 2** (self.relenum - 1)
        if BinReleNumber & OldState != BinReleNumber:
            NewValue = OldState + BinReleNumber
            bus.write_byte_data(DEVICE,OLATA,NewValue)
            return "ok"
        else:
            return "already done"
        return "ok"
            
    def Toggle(self):
        if self.Read_state() == "on":
            self.Off()
        else:
            self.On()
        return "ok"
            
    def Text(self):
        text = font.render(str(self.name) + " " + str(self.Read_state()), True, (0, 128, 0))
        return text
         
class Tube(object):
    def __init__(self, name,temp_probe,rele,val_min_temp,servo=None):
        self.name = name
        self.temp_probe = temp_probe
        self.rele = rele
        self.val_min_temp = val_min_temp
        self.servo = servo
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Tube: %s>" % self
        
    def IsHot(self):
        temp = self.temp_probe.readadc()
        minTemp = self.val_min_temp
        return int(temp) >= int(minTemp)
        
    def Text(self):
        if self.servo != None:
            text = str(self.name) + " " + str(self.temp_probe)+ " " + str(self.temp_probe.readadc()) + " " + str(self.rele)+ " " + str(self.rele.Read_state()) + " " + str(self.servo) + " " + str(self.servo.State())
            #text = font.render(str(self.name) + " " + str(self.temp_probe)+ " " + str(self.temp_probe.readadc()) + " " + str(self.rele)+ " " + str(self.rele.Read_state()) + " " + str(self.servo) + " " + str(self.servo.State()), True, (0, 128, 0))
        else:
            text = str(self.name) + " " + str(self.temp_probe)+ " " + str(self.temp_probe.readadc()) + " " + str(self.rele)+ " " + str(self.rele.Read_state())
            #text = font.render(str(self.name) + " " + str(self.temp_probe)+ " " + str(self.temp_probe.readadc()) + " " + str(self.rele)+ " " + str(self.rele.Read_state()), True, (0, 128, 0))
        return text
     
#create object

#rele
rele1 = Rele("rele",1)
rele2 = Rele("rele",2)
rele3 = Rele("rele",3)
rele4 = Rele("rele",4)
rele5 = Rele("rele",5)

#servo
#servoMin = 220  # Min 
#servoMax = 420  # Max 
servo1 = Servo("servo",220,420,0)
servo2 = Servo("servo",220,420,1)

#temperature
temp1 = TemperatureProbe("temp",0)
temp2 = TemperatureProbe("temp",1)
temp3 = TemperatureProbe("temp",2)
temp4 = TemperatureProbe("temp",3)

#display grid
firstCol = 0
secondCol = 120
thirdCol = 240
Cols = [firstCol,secondCol,thirdCol]

firstRow = 20
secondRow = 65
thirdRow = 110
fourthRow = 155
fifthRow = 200
Rows = [firstRow,secondRow,thirdRow,fourthRow,fifthRow]

Tube1 = Tube("Tube 1",temp1,rele1,"4",servo1)
Tube2 = Tube("Tube 2",temp2,rele2,"4",servo2)
Tube3 = Tube("Tube 3",temp3,rele3,"4")
Tube4 = Tube("Tube 4",temp4,rele4,"4")

Tubes = [Tube1, Tube2, Tube3, Tube4]
tube_number = 0
ActualTube = Tubes[tube_number]
while not done:
    
    screen.fill((255, 255, 255))
    # read buttons
    
    NewState = bus.read_byte_data(DEVICE,GPIOB)
    if (NewState != OldState) & (NewState != 255):
        if NewState == 254: #1
            #change tube
            if tube_number < len(Tubes) -1 :
                tube_number += 1
            else:
                tube_number = 0
            print tube_number
            ActualTube = Tubes[tube_number]
        elif NewState == 253: #2
            if ActualTube.IsHot():
                ActualTube.rele.Toggle()
                if ActualTube.servo is not None:
                    if ActualTube.rele.Read_state() == "on":
                        ActualTube.servo.Open()
                    else:
                        ActualTube.servo.Close()
        elif NewState == 251: #3
            # change Page
            #rele3.Toggle()
            #time.sleep(1)
            pass
    OldState = NewState
    
    #tubes
    for t in Tubes:
        rele = t.rele
        servo = t.servo
        
        if t.IsHot() == False :
            if rele.Read_state() == "on":
                rele.Off ()
                if servo is not None:
                    servo.Close()
            color = (0, 0, 128) #blue
        else:
            color = (0, 128, 0)# green
         
        if t == ActualTube:
            if t.IsHot():
                color = (255, 0, 0) #red
            else:
                color = (128, 128, 0) #yellow
                
        text = font.render(t.Text(), True, color)
        screen.blit(text,(Cols[0], Rows[Tubes.index(t)]))
    
    pygame.display.flip()
    clock.tick(10)
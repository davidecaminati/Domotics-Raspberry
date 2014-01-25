import sys, pygame,time
import subprocess #ping
import smbus
import time
import urllib
import urllib2
import spidev
from Adafruit_PWM_Servo_Driver import PWM
import httplib, urllib # push notification
#SERVO#
#http://www.servodatabase.com/servo/towerpro/mg995

pwm = PWM(0x44, debug=False)# Initialise the PWM device with i2c adress
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
bus.write_byte_data(DEVICE,IODIRA,0x00) # set to output all A register
bus.write_byte_data(DEVICE,IODIRB,0xff) # set to input all B register
bus.write_byte_data(DEVICE,GPPUA,0xff) # Set PullUp resistor for output register A
bus.write_byte_data(DEVICE,GPPUB,0xff) # Set PullUp resistor for input register B
bus.write_byte_data(DEVICE,OLATA,0xff) # all A rele off
#end setting for MCP 23017#

OldState = 255 # no buttons pressed

#GAS and TEMP
GAS_CLEAN_AIR = 377 # only for note
THRESHOLDGAS = 50 # + or - for change state from alarm
gasAlarm = -1  # variable for toggle from alarm to normal -1=no alarm , 1=alarm sent, 0=still in alarm
spi = spidev.SpiDev()
spi.open(0, 0)

#screen
pygame.init()
size = width, height = 480, 234
screen = pygame.display.set_mode((size),pygame.FULLSCREEN)
clock = pygame.time.Clock()
done = False
font = pygame.font.SysFont("comicsansms", 42)
pygame.mouse.set_visible(False)

#time
now = time.strftime("%c")

def Send_push(title,pushtext):
    print title,pushtext
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",urllib.urlencode({"token": "abdf67yAvRcQufveo2nGkwKNi6xTHb","user": "u2v1vYFWvmGGNGN3Ffnn9NnCW1Y3xN","message": pushtext,"title": title}), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    return 'ok'
    
def CheckInternetConnection():
    res = subprocess.call(['ping', '-c', '1', "www.google.it"])
    if res == 0:
        return "OK"
    else:
        return "Error"
        
class Servo(object):
    def __init__(self, name, servoMin, servoMax, servonum, rele):
        self.name = name
        self.servoMin = servoMin
        self.servoMax = servoMax
        self.servonum = servonum
        self.step_slower = 0.002
        self.state = ""
        self.rele = rele
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Servo: %s>" % self
                
    def Open(self):
      self.rele.On()
      time.sleep(0.5)
      for i in range(self.servoMin,self.servoMax):
        pwm.setPWM(self.servonum, 0, i)
        time.sleep(self.step_slower)
        self.state = "Open"
      time.sleep(0.5)
      self.rele.Off()
      
    def Close(self):
      self.rele.On()
      time.sleep(0.5)
      for i in range(self.servoMax-self.servoMin):
        pwm.setPWM(self.servonum, 0,self.servoMax - i)
        time.sleep(self.step_slower)
        self.state = "Close"
      time.sleep(0.5)
      self.rele.Off()
       
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

class CurrentProbe(object):
    def __init__(self, name,adcnum,alarmVal ):
        self.name = name
        self.adcnum = adcnum
        self.alarmVal = alarmVal
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<CurrentProbe: %s>" % self
        
    def InAlarm(self):
        return self.readadc() > self.alarmVal
        
    def readadc(self):
            # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        if self.adcnum > 7 or self.adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + self.adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        #debug in some case, strange, but after read the pullup resistor register fail, need to be re set
        #bus.write_byte_data(DEVICE,GPPUB,0xff) # Set PullUp resistor for input register
        #debug
        adjust = adcout - 330 #330 = 3.3 Volt base
        return adcout
        
    def Text(self):
        text = str(self.name) + " " + str(self.readadc())+ " mA"
        return text
        
class GasProbe(object):
    def __init__(self, name,adcnum,alarmVal ):
        self.name = name
        self.adcnum = adcnum
        self.alarmVal = alarmVal
    
    def InAlarm(self):
        return self.readadc() > self.alarmVal
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<GasProbe: %s>" % self
        
    def readadc(self):
            # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        if self.adcnum > 7 or self.adcnum < 0:
            return -1
        r = spi.xfer2([1, 8 + self.adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        #debug in some case, strange, but after read the pullup resistor register fail, need to be re set
        #bus.write_byte_data(DEVICE,GPPUB,0xff) # Set PullUp resistor for input register
        #debug
        return adcout
        
    def Text(self):
        text = str(self.name) + " " + str(self.readadc())
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
rele6 = Rele("rele",6)
rele7 = Rele("rele",7) #servo 2
rele8 = Rele("rele",8) #servo 1

#servo      servoMin = 220  servoMax = 420  
servo1 = Servo("servo",220,420,1,rele8)
servo2 = Servo("servo",220,420,0,rele7)

#temperature
temp1 = TemperatureProbe("temp",0)
temp2 = TemperatureProbe("temp",1)
temp3 = TemperatureProbe("temp",2)
temp4 = TemperatureProbe("temp",3)

#current
#current1 = CurrentProbe("current",5,5000)

#gas
gas1 = GasProbe("Gas",4,800)

#display grid
firstCol = 0
secondCol = 120
thirdCol = 240
fourthCol = 360
fifthCol = 400
Cols = [firstCol,secondCol,thirdCol,fourthCol,fifthCol]

firstRow = 20
secondRow = 65
thirdRow = 110
fourthRow = 155
fifthRow = 200
Rows = [firstRow,secondRow,thirdRow,fourthRow,fifthRow]

#Tubes
Tube1 = Tube("Tube 1",temp1,rele1,"-2",servo2)
Tube2 = Tube("Tube 2",temp2,rele2,"-2",servo1)
Tube3 = Tube("Tube 3",temp3,rele3,"-2")
Tube4 = Tube("Tube 4",temp4,rele4,"-2")

Tubes = [Tube1, Tube2, Tube3, Tube4]
#close all servo on startup
for t in Tubes:
    if t.servo is not None:
        t.servo.Close()     
        
tube_number = 0
ActualTube = Tubes[tube_number]
    
n = 0
connection = CheckInternetConnection()

while not done:
    screen.fill((255, 255, 255)) #white
    
    # read buttons
    NewState = bus.read_byte_data(DEVICE,GPIOB)
    if (NewState != OldState) & (NewState != 255):
        if NewState == 254: #1
            #change tube
            if tube_number < len(Tubes) -1 :
                tube_number += 1
            else:
                tube_number = 0
            #print tube_number
            ActualTube = Tubes[tube_number]
        elif NewState == 253: #2
            # Toggle
            if ActualTube.IsHot():
                ActualTube.rele.Toggle()
                if ActualTube.servo is not None:
                    if ActualTube.rele.Read_state() == "on":
                        ActualTube.servo.Open()
                    else:
                        ActualTube.servo.Close()
        elif NewState == 251: #3
            # change Page
            pass
    OldState = NewState
    
    #tubes logic
    for t in Tubes:
        rele = t.rele
        servo = t.servo
        if t.IsHot() == False :
            if rele.Read_state() == "on":
                rele.Off ()
                if servo is not None:
                    servo.Close()
            colorTube = (0, 0, 128) #blue
        else:
            colorTube = (0, 128, 0)# green
         
        if t == ActualTube:
            if t.IsHot():
                colorTube = (255, 0, 0) #red
            else:
                colorTube = (128, 128, 0) #yellow
                
        textTube = font.render(t.Text(), True, colorTube)
        screen.blit(textTube,(Cols[0], Rows[Tubes.index(t)]))
        
    if gas1.InAlarm():
        colorGas = (255,0,0) #red for alarm
        if gasAlarm != 1: # we need to comunicate alarm
            gasAlarm = 1
            #send push notification
            Send_push("alarm","Co2 too High")
    else:
        colorGas = (0,0,128) #blue, no alarm
        if gasAlarm == 1:
            gasAlarm = -1 
            #send push notification alarm off
            Send_push("alarm","Co2 OK")
            
    #current
    #textCurrent = font.render(current1.Text(), True, colorGas)
    #screen.blit(textCurrent,(Cols[2], Rows[len(Tubes)]))
    
    #time
    ## date and time representation
    #print "Current date & time " + time.strftime("%c")
    ## Only date representation
    #print "Current date "  + time.strftime("%x")
    ## Only time representation
    #print "Current time " + time.strftime("%X")
    ## Display current date and time from now variable 
    #print ("Current time %s"  % now )
    textTime = font.render("Time %s"  % time.strftime("%X"), True, (0,0,128))
    screen.blit(textTime,(Cols[1], Rows[len(Tubes)]))
    
    #gas
    textGas = font.render(gas1.Text(), True, colorGas)
    screen.blit(textGas,(Cols[0], Rows[len(Tubes)]))
    
    
    #Internet
    if connection == "Error":
        colorInternet = (255, 0, 0) #red
    else:
        colorInternet = (0,0,128) #blue
    textInternet = font.render(connection, True, colorInternet)
    screen.blit(textInternet,(Cols[4], Rows[len(Tubes)]))
    
    
    pygame.display.flip()
    clock.tick(10)
    
    #check internet connection
    n += 1
    if n > 10000 :
        print "test"
        n = 0
        connection = CheckInternetConnection()
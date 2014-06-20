import smbus
import time
import urllib
import urllib2
import looper
import threading

    
# IODIRA   0x00   // IO direction  (0 = output, 1 = input (Default))
# IODIRB   0x01
# IOPOLA   0x02   // IO polarity   (0 = normal, 1 = inverse)
# IOPOLB   0x03
# GPINTENA 0x04   // Interrupt on change (0 = disable, 1 = enable)
# GPINTENB 0x05
# DEFVALA  0x06   // Default comparison for interrupt on change (interrupts on opposite)
# DEFVALB  0x07
# INTCONA  0x08   // Interrupt control (0 = interrupt on change from previous, 1 = interrupt on change from DEFVAL)
# INTCONB  0x09
# IOCON    0x0A   // IO Configuration: bank/mirror/seqop/disslw/haen/odr/intpol/notimp
# IOCON 0x0B  // same as 0x0A
# GPPUA    0x0C   // Pull-up resistor (0 = disabled, 1 = enabled)
# GPPUB    0x0D
# INFTFA   0x0E   // Interrupt flag (read only) : (0 = no interrupt, 1 = pin caused interrupt)
# INFTFB   0x0F
# INTCAPA  0x10   // Interrupt capture (read only) : value of GPIO at time of last interrupt
# INTCAPB  0x11
# GPIOA    0x12   // Port value. Write to change, read to obtain value
# GPIOB    0x13
# OLLATA   0x14   // Output latch. Write to latch output.
# OLLATB   0x15

bus = smbus.SMBus(1)  # Rev 1 Pi uses 0
 
DEVICE = 0x24 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register for port A
IODIRB = 0x01 # Pin direction register for port B
OLATA  = 0x14 # Register for outputs for port A
OLATB  = 0x15 # Register for outputs for port B
GPIOA  = 0x12 # Register for inputs for port A
GPIOB  = 0x13 # Register for inputs for port B
GPPUA  = 0x0C # Pull-up resistor (0 = disabled, 1 = enabled)
GPPUB  = 0x0D # Pull-up resistor (0 = disabled, 1 = enabled)
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRA,0x3F) #00111111 A
bus.write_byte_data(DEVICE,IODIRB,0x00) #00000000 B

#Url for change state of reles
urlForToggle = 'http://192.168.0.202:5000/reletoggle/'
#Url for read state of rele
urlForState = 'http://192.168.0.202:5000/relestate/'
#Url for read state of all reles
urlForStateAll = 'http://192.168.0.202:5000/relestateall/'
#Url for timer 
urlForTimer = 'http://192.168.0.202:5000/reletimer/'
#Url for dimm on
urlForDimmOn = 'http://192.168.0.202:5000/reledimmon/'
#Url for dimm off
urlForDimmOff = 'http://192.168.0.202:5000/reledimmoff/'
#urlForMultiOff
urlForMultiOff = 'http://192.168.0.202:5000/multireleoff/' # need 5 number
#urlForMultiOn
urlForMultiOn = 'http://192.168.0.202:5000/multireleon/' # need 5 number

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0xC0) #11000000 A
bus.write_byte_data(DEVICE,OLATB,0x00) #00000000 B
# Set PullUp resistor for input register
bus.write_byte_data(DEVICE,GPPUA,0xFF) #11111111 A
bus.write_byte_data(DEVICE,GPPUB,0xC0) #11000000 B

RELE_ENTRANCE = 4
RELE_KITCHEN = 8
RELE_LOUNGE = 16
RELE_LOUNGE_DIM = 1


BUTTON_SALA_SX = 61       
BUTTON_CUCINA = 62
BUTTON_SALA_DX = 59
BUTTON_INGRESSO_DX = 55
BUTTON_INGRESSO_SX = 47

#color for led green for all
#bus.write_byte_data(DEVICE,GPIOB,0b10101010)
#bus.write_byte_data(DEVICE,GPIOA,0b10000000)

model = looper.ValueModel()


#start classes

class LampType():
    Halogen = 0
    Cfl = 1
    Mh = 2
    Led = 3
    Incandescent = 4
    Unknow = 5
    
class LedColor():
    Off = 0
    Red = 1
    Green = 2
    
class ButtonsState():
    Released = 0
    Pressed = 1
    StillPressed = 2
    LongPressed = 3
    

class Home(object):
    
    def __init__(self, name, roomlist = []):
        self.name = name
        self.roomlist = roomlist
                
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Home: %s>" % self
   
   
class Room(object):
    def __init__(self, name, lamplist = [], buttonlist = [],sensorlist = [],actuatorlist = [], doorlist = []):
        self.name = name
        self.lamplist = lamplist
        self.buttonlist = buttonlist
        self.sensorlist = sensorlist
        self.actuatorlist = actuatorlist
        self.doorlist = doorlist
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Room: %s>" % self
   
    def LightsOff(self):
        for l in self.lamplist:
            l.off()
            
    def LightsOn(self):
        for l in self.lamplist:
            l.on()
            
    def LightsToggle(self):
        for l in self.lamplist:
            l.toggle()
        
        
class Door(object):
    def __init__(self, name, position, releOn):
        self.name = name
        self.position = position
        self.releOn = releOn
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<lamp: %s>" % self 
     
    def open(self):
        response = urllib2.urlopen(urlForTimer + str(self.releOn) + "/500")
        html = response.read()
        return "ok"

     
class Lamp(object):
    def __init__(self, name, type, position, releOn, isdimmable, releDimm):
        self.name = name
        self.type = type
        self.position = position
        self.isdimmable = isdimmable
        self.releOn = releOn
        self.releDimm = releDimm
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<lamp: %s>" % self
   
    def read_state(self):
        response = urllib2.urlopen(urlForState + str(self.releOn))
        html = response.read()
        return html
    
    def off(self):
        if self.read_state() == "on":
            response = urllib2.urlopen(urlForToggle + str(self.releOn))
            html = response.read()
            return "ok"
        else:
            return "already off"
        
    def on(self):
        if self.read_state() != "on":
            response = urllib2.urlopen(urlForToggle + str(self.releOn))
            html = response.read()
            return "ok"
        else:
            return "already on"
            
    def toggle(self):
        oldState = self.read_state()
        response = urllib2.urlopen(urlForToggle + str(self.releOn))
        html = response.read()
        #time.sleep(0.1)
        if self.read_state() != oldState:
            return "ok"
        else:
            return "malfunction"
        
    def startDimm(self):
        if self.isdimmable:
            response = urllib2.urlopen(urlForDimmOn + str(self.releDimm) )
            html = response.read()
            return "ok"
        else:
            return "not dimmable"
        
    def stopDimm(self):
        if self.isdimmable:
            response = urllib2.urlopen(urlForDimmOff + str(self.releDimm) )
            html = response.read()
            return "ok"
        else:
            return "not dimmable"
    
class MainController(object):    
    
    def __init__(self, name,home,urlForToggle,urlForMultiOff,urlForMultiOn):
        self.name = name
        self.home = home
        self.urlForToggle = urlForToggle
        self.urlForMultiOff = urlForMultiOff
        self.urlForMultiOn = urlForMultiOn
        self.lampList = []
        self.__popolateLampList__()
        
                  
    def group_iter(self,iterator, n=1):
        """ Given an iterator, it returns sub-lists made of n items
        (except the last that can have len < n)
        inspired by http://countergram.com/python-group-iterator-list-function"""
        accumulator = []
        for item in iterator:
            accumulator.append(item)
            if len(accumulator) == n: # tested as fast as separate counter
                yield accumulator
                accumulator = [] # tested faster than accumulator[:] = []
                # and tested as fast as re-using one list object
        if len(accumulator) != 0:
            yield accumulator

    def __popolateLampList__(self):
        for r in self.home.roomlist:
            for l in r.lamplist:
                self.lampList.append(l.releOn)
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Button: %s>" % self
    
    def LightsOff(self):
        if len(self.lampList) > 5:
            #need split
            groups = self.group_iter(self.lampList,5)
            for g in groups:
                # i need to be sure than i can take 5 element 
                raw = g*5
                response = urllib2.urlopen(urlForMultiOff + str(raw[0]) + "/"  + str(raw[1]) + "/" + str(raw[2]) + "/" + str(raw[3]) + "/" + str(raw[4]))
                html = response.read()
                return "ok"
        else:
            #send list to webservice
            if len(self.lampList) != 0:
                raw = self.lampList * 5
                response = urllib2.urlopen(urlForMultiOff + str(raw[0]) + "/"  + str(raw[1]) + "/" + str(raw[2]) + "/" + str(raw[3]) + "/" + str(raw[4]))
                html = response.read()
                return "ok"
            else:
                return "allready done"
            
    def LightsOn(self):
        if len(self.lampList) > 5:
            #need split
            groups = self.group_iter(self.lampList,5)
            for g in groups:
                # i need to be sure than i can take 5 element 
                raw = g*5
                response = urllib2.urlopen(urlForMultiOn + str(raw[0]) + "/"  + str(raw[1]) + "/" + str(raw[2]) + "/" + str(raw[3]) + "/" + str(raw[4]))
                html = response.read()
                return "ok"
        else:
            #send list to webservice
            if len(self.lampList) != 0:
                raw = self.lampList * 5
                response = urllib2.urlopen(urlForMultiOn + str(raw[0]) + "/"  + str(raw[1]) + "/" + str(raw[2]) + "/" + str(raw[3]) + "/" + str(raw[4]))
                html = response.read()
                return "ok"
            else:
                return "allready done"


#"ButtonXBee_DX",0,0b00000100,0b00001000,model,Launge
class Button(object):
    def __init__(self, name, inputpin,BinLedNumberRED,BinLedNumberGREEN,model,controlled):
        self.name = name
        self.inputpin = inputpin
        self.BinLedNumberRED = BinLedNumberRED
        self.BinLedNumberGREEN = BinLedNumberGREEN
        self.model = model
        model.events.Pressed += self.Pressed
        model.events.StillPressed += self.StillPressed
        model.events.LongPressed += self.LongPressed
        model.events.Released += self.Released
        model.events.Voice += self.Voice
        self.controlled = controlled
        self._old_state = ButtonsState.Released
        
    def Voice(self):
        if self.model.get() == self.name : # 'Vocal'
            #print str(self.model.getVocal())
            #voice command grom Minix
            if str(self.model.getVocal()) == 'SAMANTHA':
                print "SAMANTA"
                try:
                    response = urllib2.urlopen("http://192.168.0.114:8080/getQuestion", timeout = 1)
                except socket.timeout, e:
                    # For Python 2.7
                     urllib2.urlopen("http://192.168.0.114:8080/speak/scusa%20non%20trovo%20nulla")
            
            
            #print str(self.model.getVocal()).split()
            if str(self.model.getVocal()).split()[0] == 'Temperature':
                print "Temperature"
                try:
                    response = urllib2.urlopen("http://192.168.0.208:5000/setredis/Temperature/" + str(self.model.getVocal()).split()[1], timeout = 1)
                except socket.timeout, e:
                    # For Python 2.7
                    #urllib2.urlopen("http://192.168.0.114:8080/speak/scusa%20non%20trovo%20nulla")
                    pass
                    
            #print str(self.model.getVocal()).split()
            if str(self.model.getVocal()).split()[0] == 'Light':
                print "Light"
                try:
                    response = urllib2.urlopen("http://192.168.0.208:5000/setredis/Light/" + str(self.model.getVocal()).split()[1], timeout = 1)
                except socket.timeout, e:
                    # For Python 2.7
                    #urllib2.urlopen("http://192.168.0.114:8080/speak/scusa%20non%20trovo%20nulla")
                    pass
                    
            if str(self.model.getVocal()) == 'TEMPERATURA':
                print "TEMPERATURA"
                try:
                    response = urllib2.urlopen("http://192.168.0.208:5000/getredis/Temperature", timeout = 1)

                    speak = urllib2.urlopen("http://192.168.0.114:8080/speak/" + response.read() + "%20gradi")
                except socket.timeout, e:
                    # For Python 2.7
                     urllib2.urlopen("http://192.168.0.114:8080/speak/scusa%20non%20trovo%20nulla")
            
            
            if str(self.model.getVocal()) == 'LUCE_INGRESSO':
                Lamp_holder_entrance.toggle()
            elif str(self.model.getVocal()) == 'LUCE_SALA':
                Lamp_holder_lounge.toggle()
            elif str(self.model.getVocal()) == 'LUCE_CUCINA':
                Lamp_holder_kitchen.toggle()
            elif str(self.model.getVocal()) == 'SPEGNI_TUTTO':
                for room in MyHome.roomlist:
                    for lamp in room.lamplist:
                        lamp.off()

            print str(self.model.getVocal())
            if str(self.model.getVocal()) == 'LUCE_INGRESSO_ONDI':
                Lamp_holder_entrance.toggle()
            elif str(self.model.getVocal()) == 'LUCE_SALA_ONDI':
                Lamp_holder_lounge.toggle()
            elif str(self.model.getVocal()) == 'LUCE_CUCINA_ONDI':
                Lamp_holder_kitchen.toggle()
            elif str(self.model.getVocal()) == 'SPEGNI_TUTTO_ONDI':
                for room in MyHome.roomlist:
                    for lamp in room.lamplist:
                        lamp.off()

            self._old_state = ButtonsState.Pressed
            CheckColorForLeds()
            #else:
            #    print 'not match' , self.model.getVocal()
            
            
        
        
    def Pressed(self,Xbee=False):
        if Xbee:
            self._old_state = ButtonsState.Released
            
        if self.model.get() == self.name :
            if isinstance(self.controlled, Lamp):
                if self._old_state == ButtonsState.Released:
                    lamp = self.controlled
                    if lamp.isdimmable:
                        pass # none
                    else:
                        lamp.toggle()
            if isinstance(self.controlled, Room):
                if self._old_state == ButtonsState.Released:
                    for lamp in self.controlled.lamplist:
                        if lamp.isdimmable:
                            pass # none
                        else:
                            lamp.toggle()
            if isinstance(self.controlled, Home):
                if self._old_state == ButtonsState.Released:
                    for room in self.controlled.roomlist:
                        for lamp in room.lamplist:
                            if lamp.isdimmable:
                                pass # none
                            else:
                                lamp.off()
            
            self._old_state = ButtonsState.Pressed
            CheckColorForLeds()
            
    def StillPressed(self):
        if self.model.get() == self.name :
            #print self.name + " StillPressed"
            if isinstance(self.controlled, Lamp):
                #print "Lamp StillPressed"
                if self._old_state == ButtonsState.Pressed:
                    lamp = self.controlled
                    if lamp.isdimmable:
                        lamp.on()
                if self._old_state == ButtonsState.Released:
                    lamp = self.controlled
                    if lamp.isdimmable:
                        lamp.off()
            if isinstance(self.controlled, Room):
                #print "Room StillPressed"
                if self._old_state == ButtonsState.Pressed:
                    for lamp in self.controlled.lamplist:
                        if lamp.isdimmable:
                            lamp.on()
                if self._old_state == ButtonsState.Released:
                    if lamp.isdimmable:
                        lamp.off()
            if isinstance(self.controlled, Home):
                #print "Home StillPressed"
                if self._old_state == ButtonsState.Pressed:
                    for room in self.controlled.roomlist:
                        for lamp in room.lamplist:
                                if  lamp.isdimmable:
                                    lamp.on()
                if self._old_state == ButtonsState.Released:
                    if lamp.isdimmable:
                        lamp.off()
            self._old_state = ButtonsState.StillPressed
            CheckColorForLeds()
            
    def LongPressed(self):
        if self.model.get() == self.name :
            #print self.name + " LongPressed"
            if isinstance(self.controlled, Lamp):
                #print "Lamp LongPressed"
                lamp = self.controlled
                if self._old_state == ButtonsState.StillPressed:
                    if lamp.isdimmable:
                        lamp.startDimm()
            if isinstance(self.controlled, Room):
                #print "Room LongPressed"
                for lamp in self.controlled.lamplist:
                    if self._old_state == ButtonsState.StillPressed:
                        if lamp.isdimmable:
                            lamp.startDimm()
            if isinstance(self.controlled, Home):
                #print "Home LongPressed"
                for room in self.controlled.roomlist:
                    for lamp in room.lamplist:
                        if self._old_state == ButtonsState.StillPressed:
                            if  lamp.isdimmable:
                                lamp.startDimm()
            self._old_state = ButtonsState.StillPressed
            CheckColorForLeds()
            
    def Released(self):
        if self.model.get() == self.name :
            #print self.name + " Released"
            if isinstance(self.controlled, Lamp):
                #print "Lamp Released"
                lamp = self.controlled
                if self._old_state == ButtonsState.LongPressed:
                    if lamp.isdimmable:
                        lamp.stopDimm()
                if self._old_state == ButtonsState.Pressed:
                    if lamp.isdimmable:
                        lamp.off()
            if isinstance(self.controlled, Room):
                #print "Room Released"
                for lamp in self.controlled.lamplist:
                    if self._old_state == ButtonsState.LongPressed:
                        if lamp.isdimmable:
                            lamp.stopDimm()
                    if self._old_state == ButtonsState.Pressed:
                        if lamp.isdimmable:
                            lamp.off()
            if isinstance(self.controlled, Home):
                #print "Home Released"
                for room in self.controlled.roomlist:
                    for lamp in room.lamplist:
                        if self._old_state == ButtonsState.LongPressed:
                            if lamp.isdimmable:
                                lamp.stopDimm()
                        if self._old_state == ButtonsState.Pressed:
                            if lamp.isdimmable:
                                lamp.off()
            self._old_state = ButtonsState.Released
            CheckColorForLeds()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Button: %s>" % self
   
    def SetLedColorB(self, Color):
        OldStateB = bus.read_byte_data(DEVICE,GPIOB)
        NewBinLedNumber = 0b00000000
        if Color == LedColor.Red:
            NewBinLedNumber =  (OldStateB & ( ~ self.BinLedNumberGREEN )) | self.BinLedNumberRED
        elif Color == LedColor.Green:
            NewBinLedNumber =  (OldStateB & ( ~ self.BinLedNumberRED)) | self.BinLedNumberGREEN 
        else:
            NewBinLedNumber =  OldStateB & ( ~ (self.BinLedNumberRED |  self.BinLedNumberGREEN))
        bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
    
    def SetLedColorA(self, Color):
        OldStateA = bus.read_byte_data(DEVICE,GPIOA)
        NewBinLedNumber = 0b00000000
        if Color == LedColor.Red:
            NewBinLedNumber =  (OldStateA & ( ~ self.BinLedNumberGREEN )) | self.BinLedNumberRED
        elif Color == LedColor.Green:
            NewBinLedNumber =  (OldStateA & ( ~ self.BinLedNumberRED)) | self.BinLedNumberGREEN 
        else:
            NewBinLedNumber =  OldStateA & ( ~ (self.BinLedNumberRED |  self.BinLedNumberGREEN))
        bus.write_byte_data(DEVICE,GPIOA,NewBinLedNumber)
            
# ---- door -----
Entrance_door = Door("Entrance Door", "Entrance", 8)

# ---- lamp -----
Lamp_holder_lounge_dimm = Lamp("lamp holder dimm",LampType.Led,"lounge",1,True,6)
Lamp_holder_entrance = Lamp("lamp holder",LampType.Led,"Entrance",3,False,0)
Lamp_holder_kitchen = Lamp("lamp holder",LampType.Led,"Kitchen",4,False,0)
Lamp_holder_lounge = Lamp("lamp holder",LampType.Led,"lounge",5,False,0)

#Lamp_holder_lounge.on()
#Lamp_holder_lounge.dimm()
#Lights = [Lamp_holder_lounge,lampadario_ingresso,lampadario_cucina,lampadario_sala]
#for l in Lights:
#    l.on()
# Create Room
Launge = Room("Launge",[Lamp_holder_lounge_dimm,Lamp_holder_lounge])
Kitchen = Room("Kitchen",[Lamp_holder_kitchen])
Entrance = Room("Entrance",[Lamp_holder_entrance],None,None,None,Entrance_door)
#Create Home
MyHome = Home("Home",[Launge,Kitchen,Entrance])
MyController = MainController("Main Controller",MyHome,urlForToggle,urlForMultiOff,urlForMultiOn)


ButtonLaunge_SX = Button("ButtonLaunge_SX",0,0b00000100,0b00001000,model,Launge)
ButtonLaunge_DX = Button("ButtonLaunge_DX",0,0b00010000,0b00100000,model,Entrance)
ButtonKitchen = Button("ButtonKitchen",0,0b00000001,0b00000010,model,Kitchen)
ButtonEntrance_SX = Button("ButtonEntrance_SX",0,0b01000000,0b10000000,model,MyHome)
ButtonEntrance_DX = Button("ButtonEntrance_DX",0,0b01000000,0b10000000,model,Entrance) #A

ButtonXBee_SX = Button("ButtonXBee_SX",0,0b00000100,0b00001000,model,Launge)
ButtonXBee_DX = Button("ButtonXBee_DX",0,0b00000100,0b00001000,model,Kitchen)
ButtonXBee_Vocal = Button("Vocal",0,0b00000100,0b00001000,model,Kitchen)

model.daemon = True # non blocking thread
model.start()


def CheckColorForLeds():
    #read state
    response = urllib2.urlopen(urlForStateAll)
    html = response.read()
    statevalue = int(html)
    
    if (statevalue & RELE_KITCHEN) == RELE_KITCHEN:
        ButtonKitchen.SetLedColorB(LedColor.Green)
    else:
        ButtonKitchen.SetLedColorB(LedColor.Red)
        
    if (statevalue & RELE_ENTRANCE) == RELE_ENTRANCE:
        ButtonLaunge_DX.SetLedColorB(LedColor.Green)
        ButtonEntrance_DX.SetLedColorB(LedColor.Green)
    else:
        ButtonLaunge_DX.SetLedColorB(LedColor.Red)
        ButtonEntrance_DX.SetLedColorB(LedColor.Red)
        
    if ((statevalue & RELE_LOUNGE) == RELE_LOUNGE) & (statevalue & RELE_LOUNGE_DIM) == RELE_LOUNGE_DIM:
        ButtonLaunge_SX.SetLedColorB(LedColor.Green)
    else:
        ButtonLaunge_SX.SetLedColorB(LedColor.Red)
        
        
    if ((statevalue & RELE_LOUNGE) == RELE_LOUNGE) &  ((statevalue & RELE_ENTRANCE) == RELE_ENTRANCE) & ((statevalue & RELE_KITCHEN) == RELE_KITCHEN) & ((statevalue & RELE_LOUNGE_DIM) == RELE_LOUNGE_DIM): 
        ButtonEntrance_SX.SetLedColorA(LedColor.Green) 
    else:
        ButtonEntrance_SX.SetLedColorA(LedColor.Red)


while True:
    CheckColorForLeds()
    time.sleep(5)

        

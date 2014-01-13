import smbus
import time
import urllib
import urllib2



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

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0xC0) #11000000 A
bus.write_byte_data(DEVICE,OLATB,0x00) #00000000 B
# Set PullUp resistor for input register
bus.write_byte_data(DEVICE,GPPUA,0xFF) #11111111 A
bus.write_byte_data(DEVICE,GPPUB,0xC0) #11000000 B

RELE_INGRESSO = 4
RELE_CUCINA = 8
RELE_SALA = 16

BUTTON_SALA_SX = 61       
BUTTON_CUCINA = 62
BUTTON_SALA_DX = 59
BUTTON_INGRESSO_DX = 55
BUTTON_INGRESSO_SX = 47

#color for led
bus.write_byte_data(DEVICE,GPIOB,0b10101010)
bus.write_byte_data(DEVICE,GPIOA,0b10000000)

#reset button state
BottoneSala_SX_oldstate = False
BottoneSala_DX_oldstate = False
BottoneCucina_oldstate = False
BottoneIngresso_SX_oldstate = False
BottoneIngresso_DX_oldstate = False

######################################################################
## 
## Events
## 
######################################################################

class Events:
   def __getattr__(self, name):
      if hasattr(self.__class__, '__events__'):
         assert name in self.__class__.__events__, \
                "Event '%s' is not declared" % name
      self.__dict__[name] = ev = _EventSlot(name)
      return ev
   def __repr__(self): return 'Events' + str(list(self))
   __str__ = __repr__
   def __len__(self): return NotImplemented
   def __iter__(self):
      def gen(dictitems=self.__dict__.items()):
         for attr, val in dictitems:
            if isinstance(val, _EventSlot):
               yield val
      return gen()

class _EventSlot:
   def __init__(self, name):
      self.targets = []
      self.__name__ = name
   def __repr__(self):
      return 'event ' + self.__name__
   def __call__(self, *a, **kw):
      for f in self.targets: f(*a, **kw)
   def __iadd__(self, f):
      self.targets.append(f)
      return self
   def __isub__(self, f):
      while f in self.targets: self.targets.remove(f)
      return self

######################################################################
## 
## Demo
## 
######################################################################

if __name__ == '__main__':

   class MyEvents(Events):
      __events__ = ('OnChange', )

   class ValueModel(object):
      def __init__(self):
         self.events = MyEvents()
         self.__value = None
      def __set(self, value):
         if (self.__value == value): return
         self.__value = value
         self.events.OnChange()
         ##self.events.OnChange2() # would fail
      def __get(self):
         return self.__value
      Value = property(__get, __set, None, 'The actual value')

   class SillyView(object):
      def __init__(self, model):
         self.model = model
         model.events.OnChange += self.DisplayValue
         ##model.events.OnChange2 += self.DisplayValue # would raise exeception
      def DisplayValue(self):
         print self.model.Value


   model = ValueModel()
   view = SillyView(model)

   print '\n--- Events Demo ---'
   # Events in action
   for i in range(5):
      model.Value = 2*i + 1
   # Events introspection
   print model.events
   for event in model.events:
      print event


class Home:
    def __init__(self, name, roomlist = []):
        self.name = name
        self.roomlist = roomlist
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Home: %s>" % self
   
    def LightsOff(self):
        for r in self.roomlist:
            for l in r.lamplist:
                l.off()
                
    def LightsOn(self):
        for r in self.roomlist:
            for l in r.lamplist:
                l.on()
                
    def LightsToggle(self):
        for r in self.roomlist:
            for l in r.lamplist:
                l.toggle()
   
#start classes
class Room:
    def __init__(self, name, lamplist = [], buttonlist = [],sensorlist = [],actuatorlist = []):
        self.name = name
        self.lamplist = lamplist
        self.buttonlist = buttonlist
        self.sensorlist = sensorlist
        self.actuatorlist = actuatorlist
        
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
        
class Lamp:
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
        
    def dimm(self,value=3000):
        if self.isdimmable:
            print value
            response = urllib2.urlopen(urlForTimer + str(self.releDimm) + "/" + str(value))
            html = response.read()
            return "ok"
        else:
            return "not dimmable"
 
 
 
 

class MyEvents(Events):
    __events__ = ('OnChange', )
      
class Button(object):
    myaddress = 61
    def __init__(self, name, inputpin,BinLedNumberRED,BinLedNumberGREEN,MYADDRESS):
        self.name = name
        self.inputpin = inputpin
        self.BinLedNumberRED = BinLedNumberRED
        self.BinLedNumberGREEN = BinLedNumberGREEN
        self.__value = None
        myaddress = MYADDRESS
        self.events = MyEvents()
        # Read state of GPIOA register
        while True:
            MySwitchA = bus.read_byte_data(DEVICE,GPIOA) & 0b00111111
            print "MySwitchA %s" % MySwitchA
            #print "myaddress %s" % myaddress
            if MySwitchA == myaddress :
                #print "oooooooooooooooooooooooo" 
                self.events.OnChange()
        
    def __set(self, value):
        if (self.__value == value): return
        self.__value = value
        self.events.OnChange()
        ##self.events.OnChange2() # would fail
    def __get(self):
        return self.__value
        Value = property(__get, __set, None, 'The actual value')
      

        
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Button: %s>" % self
   
    def SetLedColor(self, Color):
        OldState = bus.read_byte_data(DEVICE,GPIOB)
        NewBinLedNumber = 0b00000000
        if Color == LedColor.Red:
            NewBinLedNumber =  (OldState & ( ~ self.BinLedNumberGREEN )) | self.BinLedNumberRED
        elif Color == LedColor.Green:
            NewBinLedNumber =  (OldState & ( ~ self.BinLedNumberRED)) | self.BinLedNumberGREEN 
        else:
            NewBinLedNumber =  OldState & ( ~ (self.BinLedNumberRED |  self.BinLedNumberGREEN))
        bus.write_byte_data(DEVICE,GPIOB,NewBinLedNumber)
    
    def SetLedColorA(self, Color):
        OldState = bus.read_byte_data(DEVICE,GPIOA)
        NewBinLedNumber = 0b00000000
        if Color == LedColor.Red:
            NewBinLedNumber =  (OldState & ( ~ self.BinLedNumberGREEN )) | self.BinLedNumberRED
        elif Color == LedColor.Green:
            NewBinLedNumber =  (OldState & ( ~ self.BinLedNumberRED)) | self.BinLedNumberGREEN 
        else:
            NewBinLedNumber =  OldState & ( ~ (self.BinLedNumberRED |  self.BinLedNumberGREEN))
        bus.write_byte_data(DEVICE,GPIOA,NewBinLedNumber)

   
   
# ---- lamp -----
lampadario_sala_dimm = Lamp("lampadario",LampType.Led,"Sala dimm",1,True,6)
lampadario_ingresso = Lamp("lampadario",LampType.Led,"Ingresso",3,False,0)
lampadario_cucina = Lamp("lampadario",LampType.Led,"Cucina",4,False,0)
lampadario_sala = Lamp("lampadario",LampType.Led,"Sala",5,False,0)

#lampadario_sala_dimm.on()
#lampadario_sala_dimm.dimm()
#Lights = [lampadario_sala_dimm,lampadario_ingresso,lampadario_cucina,lampadario_sala]
#for l in Lights:
#    l.on()
# Create Room
Sala = Room("Sala",[lampadario_sala_dimm,lampadario_sala])
Cucina = Room("Cucina",[lampadario_cucina])
Ingresso = Room("Ingresso",[lampadario_ingresso])
#Create Home
Casa = Home("Casa",[Sala,Cucina,Ingresso])

#BottoneSala_SX = Button("Sala SX",0,0b00000100,0b00001000,BUTTON_SALA_SX)
#BottoneSala_DX = Button("Sala DX",0,0b00010000,0b00100000)
#BottoneCucina = Button("Cucina",0,0b00000001,0b00000010)
#BottoneIngresso_SX = Button("Ingresso SX",0,0b01000000,0b10000000)
#BottoneIngresso_DX = Button("Ingresso DX",0,0b01000000,0b10000000) #A


def CheckColorForLeds():
    #read state
    response = urllib2.urlopen(urlForStateAll)
    html = response.read()
    statevalue = int(html)
    #time.sleep(0.1)
    
    if (statevalue & RELE_CUCINA) == RELE_CUCINA:
        BottoneCucina.SetLedColor(LedColor.Green)
    else:
        BottoneCucina.SetLedColor(LedColor.Red)
        
    if (statevalue & RELE_INGRESSO) == RELE_INGRESSO:
        BottoneSala_DX.SetLedColor(LedColor.Green)
        BottoneIngresso_DX.SetLedColor(LedColor.Green)
    else:
        BottoneSala_DX.SetLedColor(LedColor.Red)
        BottoneIngresso_DX.SetLedColor(LedColor.Red)
        
    if (statevalue & RELE_SALA) == RELE_SALA:
        BottoneSala_SX.SetLedColor(LedColor.Green)
    else:
        BottoneSala_SX.SetLedColor(LedColor.Red)
        
    if ((statevalue & RELE_SALA) == RELE_SALA) &  ((statevalue & RELE_INGRESSO) == RELE_INGRESSO) & ((statevalue & RELE_CUCINA) == RELE_CUCINA):
        BottoneIngresso_SX.SetLedColorA(LedColor.Green)
    else:
        BottoneIngresso_SX.SetLedColorA(LedColor.Red)
    
i = 0

class SillyView(object):
      def __init__(self, model):
         self.model = model
         model.events.OnChange += self.DisplayValue
         ##model.events.OnChange2 += self.DisplayValue # would raise exeception
      def DisplayValue(self):
         print self.model.name
   
   
model = Button("Sala SX",0,0b00000100,0b00001000,BUTTON_SALA_SX)
view = SillyView(model)      
"""
# Loop until user presses CTRL-C
while True:
 
    # Read state of GPIOA register
    MySwitchA = bus.read_byte_data(DEVICE,GPIOA) & 0b00111111
    #print "MySwitchA %s" % MySwitchA
    if MySwitchA == BUTTON_CUCINA :
        if BottoneCucina_oldstate == False:
            # send toggle
            lampadario_cucina.toggle()
            #time.sleep(0.1)
            CheckColorForLeds()
            BottoneCucina_oldstate = True
    if MySwitchA == BUTTON_SALA_SX :
        if BottoneSala_SX_oldstate == False:
            # send toggle
            lampadario_sala.toggle()
            #time.sleep(0.1)
            CheckColorForLeds()
            BottoneSala_SX_oldstate = True
    if MySwitchA == BUTTON_SALA_DX :
        if BottoneSala_DX_oldstate == False:
            # send toggle
            lampadario_ingresso.toggle()
            #time.sleep(0.1)
            CheckColorForLeds()
            BottoneSala_DX_oldstate = True
    if MySwitchA == BUTTON_INGRESSO_DX :
        if BottoneIngresso_DX_oldstate == False:
            # send toggle
            lampadario_ingresso.toggle()
            #time.sleep(0.1)
            CheckColorForLeds()
            BottoneIngresso_DX_oldstate = True
    if MySwitchA == BUTTON_INGRESSO_SX :
        if BottoneIngresso_SX_oldstate == False:
            # send aff all light in the home
            Casa.LightsOff()
            #time.sleep(0.1)
            CheckColorForLeds()
            BottoneIngresso_SX_oldstate = True
    else:
        if BottoneSala_SX_oldstate == True:
            BottoneSala_SX_oldstate = False
        if BottoneSala_DX_oldstate == True:
            BottoneSala_DX_oldstate = False
        if BottoneIngresso_SX_oldstate == True:
            BottoneIngresso_SX_oldstate = False
        if BottoneIngresso_DX_oldstate == True:
            BottoneIngresso_DX_oldstate = False
        if BottoneCucina_oldstate == True:
            BottoneCucina_oldstate = False
        #print MySwitchA
    #time.sleep(0.1)
    # periodic update led state
    print MySwitchA
    print i
    i +=1
    if i > 1000:
        i = 0 
        CheckColorForLeds()

"""
   

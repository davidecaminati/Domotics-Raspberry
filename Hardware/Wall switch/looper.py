
import threading
import smbus
import time

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


# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0xC0) #11000000 A
bus.write_byte_data(DEVICE,OLATB,0x00) #00000000 B
# Set PullUp resistor for input register
bus.write_byte_data(DEVICE,GPPUA,0xFF) #11111111 A
bus.write_byte_data(DEVICE,GPPUB,0xC0) #11000000 B

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

class MyEvents(Events):
   __events__ = ('Pressed', 'StillPressed', 'Released')

class ValueModel(threading.Thread):
   def __init__(self):
        threading.Thread.__init__(self)
        self.events = MyEvents()
        self.__value = None
        self.set("")
        
   def set(self, value):
        #if (self.__value == value): return
        self.__value = value
        
   def get(self):
        return self.__value

   def run(self):
        Bottone_oldstate = False
        i = 0
        BUTTON_SALA_SX = 61  
        BUTTON_SALA_DX = 59     
        BUTTON_CUCINA = 62
        BUTTON_INGRESSO_DX = 55
        BUTTON_INGRESSO_SX = 47
        dict_bottoni = {61:"BUTTON_SALA_SX",59:"BUTTON_SALA_DX",62:"BUTTON_CUCINA",55:"BUTTON_INGRESSO_DX",47:"BUTTON_INGRESSO_SX"}
        while True:
            # Read state of GPIOA register
            time.sleep(0.1)
            MySwitchA = bus.read_byte_data(DEVICE,GPIOA) & 0b00111111
            if  dict_bottoni.get(MySwitchA) is not None:
                if Bottone_oldstate == False:
                    Bottone_oldstate = True
                    self.set(dict_bottoni.get(MySwitchA))
                    self.events.Pressed()
                    i = 0
                else:
                    i += 1
                    if i > 5:
                        self.set(dict_bottoni.get(MySwitchA))
                        self.events.StillPressed()
            else:
                Bottone_oldstate = False
                if self.get() != "" :
                    self.events.Released()
                    self.set("")
               
            
            

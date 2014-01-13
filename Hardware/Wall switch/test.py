import looper

import threading

model = looper.ValueModel()


class SillyView(object):
   def __init__(self, model):
      self.model = model
      model.events.Pressed += self.Pressed
      model.events.StillPressed += self.StillPressed
      model.events.Released += self.Released
      model.events.NeedCheckForColors += self.NeedCheckForColors
      
      
   def Pressed(self):
      print self.model.get(), "Pressed"
   def StillPressed(self):
      print self.model.get(), "StillPressed"
   def Released(self):
      print self.model.get(), "Released"
   def NeedCheckForColors(self):
      print self.model.get() , "NeedCheckForColors"

view = SillyView(model)

print '\n--- Events Demo ---'
# Events in action
thread1 =  model

thread1.start()
print "pippo"
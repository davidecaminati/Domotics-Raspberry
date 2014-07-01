#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// photo
int LDR_Pin = A0; //analog pin 0
int Timer_For_Send = 200; //timer
int counter_for_send = 0; // counter

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
  #include "Platform.h"
  #include "SoftwareSerial.h"
#ifndef CDC_ENABLED
  // Shield Jumper on SW
  SoftwareSerial port(12,13);
#else
  // Shield Jumper on HW (for Leonardo)
  #define port Serial1
#endif
#else // Arduino 0022 - use modified NewSoftSerial
  #include "WProgram.h"
  #include "NewSoftSerial.h"
  NewSoftSerial port(12,13);
#endif

#include "EasyVR.h"

EasyVR easyvr(port);

//Groups and Commands
enum Groups
{
  GROUP_0  = 0,
  GROUP_1  = 1,
  GROUP_16 = 16,
};

enum Group0 
{
  G0_MARVIN = 0,
};

enum Group1 
{
  G1_LUCE_SALA = 0,
  G1_LUCE_CUCINA = 1,
  G1_LUCE_INGRESSO = 2,
  G1_SPEGNI_TUTTO = 3,
  G1_TEMPERATURA = 4,
  G1_LUCE_SALA_ONDI = 5,
  G1_LUCE_CUCINA_ONDI = 6,
  G1_LUCE_INGRESSO_ONDI = 7,
  G1_SPEGNI_TUTTO_ONDI = 8,
  G1_TEMPERATURA_ONDI = 9,
  G1_SAMANTHA = 10,
};

enum Group16
{
  G16_PWD_DAVIDE = 0,
  G16_PWD_ONDINA = 1,
};


EasyVRBridge bridge;

int8_t group, idx;

void setup()
{
  
  // Start up the library
  sensors.begin();
  
  
#ifndef CDC_ENABLED
  // bridge mode?
  if (bridge.check())
  {
    cli();
    bridge.loop(0, 1, 12, 13);
  }
  // run normally
  Serial.begin(9600);
  //Serial.println("Bridge not started!");
#else
  // bridge mode?
  if (bridge.check())
  {
    port.begin(9600);
    bridge.loop(port);
  }
  //Serial.println("Bridge connection aborted!");
#endif
  port.begin(9600);

  while (!easyvr.detect())
  {
    //Serial.println("EasyVR not detected!");
    delay(1000);
  }

  easyvr.setPinOutput(EasyVR::IO1, LOW);
  //Serial.println("EasyVR detected!");
  easyvr.setTimeout(5);
  easyvr.setLanguage(1);

  //group = EasyVR::TRIGGER; //<-- start group (customize)
  group = 1; //<-- start group (customize)
}

void action();

void loop()
{
  easyvr.setPinOutput(EasyVR::IO1, HIGH); // LED on (listening)

  //Serial.print("Say a command in Group ");
  //Serial.println(group);
  easyvr.recognizeCommand(group);

  do
  {

  }
  while (!easyvr.hasFinished());
    ++counter_for_send;
    if (counter_for_send >= Timer_For_Send)
      {
      // can do some processing while waiting for a spoken command
      // call sensors.requestTemperatures() to issue a global temperature 
      // request to all devices on the bus
      sensors.requestTemperatures(); // Send the command to get temperatures
      //Serial.print("Temperature ");
      String temperature = String(sensors.getTempCByIndex(0));
      String strtemperature = "Temperature "+ temperature;
      Serial.println(strtemperature);
      

      //reset counter
      counter_for_send = 0;
      }
      
      if (counter_for_send == Timer_For_Send /2 )
      {
      //photo
      int LDRReading = 1024 - analogRead(LDR_Pin); 
      String strLDR = "Light " + String(LDRReading);
      Serial.println(strLDR);
      
      }
        
  easyvr.setPinOutput(EasyVR::IO1, LOW); // LED off

  idx = easyvr.getWord();
  if (idx >= 0)
  {
    // built-in trigger (ROBOT)
    // group = GROUP_X; <-- jump to another group X
    return;
  }
  idx = easyvr.getCommand();
  if (idx >= 0)
  {
    // print debug message
    uint8_t train = 0;
    char name[32];
    //Serial.print("Command: ");
    //Serial.print(idx);
    if (easyvr.dumpCommand(group, idx, name, train))
    {
      //Serial.print(" = ");
      Serial.println(name);
    }
    else
      //Serial.println();
    //easyvr.playSound(0, EasyVR::VOL_FULL);
    // perform some action
    action();
  }
  else // errors or timeout
  {
    //if (easyvr.isTimeout())
      //Serial.println("Timed out, try again...");
    //int16_t err = easyvr.getError();
    //if (err >= 0)
    //{
      //Serial.print("Error ");
      //Serial.println(err, HEX);
    //}
  }
}

void action()
{
    switch (group)
    {
    case GROUP_0:
      switch (idx)
      {
      case G0_MARVIN:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      }
      break;
    case GROUP_1:
      switch (idx)
      {
      case G1_LUCE_SALA:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_LUCE_CUCINA:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_LUCE_INGRESSO:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_SPEGNI_TUTTO:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_TEMPERATURA:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_LUCE_SALA_ONDI:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_LUCE_CUCINA_ONDI:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_LUCE_INGRESSO_ONDI:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_SPEGNI_TUTTO_ONDI:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_TEMPERATURA_ONDI:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G1_SAMANTHA:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      }
      break;
    case GROUP_16:
      switch (idx)
      {
      case G16_PWD_DAVIDE:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      case G16_PWD_ONDINA:
        // write your action code here
        // group = GROUP_X; <-- or jump to another group X for composite commands
        break;
      }
      break;
    }
}

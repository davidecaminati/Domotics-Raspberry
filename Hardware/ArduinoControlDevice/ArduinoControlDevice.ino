/*
 1 analog input, 3 digital input, serial output
 
 created 16 Aug. 2014
 by Davide Caminati
 */
 
// These constants won't change. 
const int analogInPin = A1;  // Analog input pin that the potentiometer is attached to
const int DigitalInPin2 = 2;  // Digital input pin that the buttonGo is attached to
const int DigitalInPin3 = 3;  // Digital input pin that the buttonStop is attached to
const int DigitalInPin4 = 4;  // Digital input pin that the buttonBack is attached to
const int pos[] = {0,417,862,976,1008,1019,1024}; // 7 step on the logarithimic resistor (1 each cm.)
const int posCount = sizeof(pos)/sizeof(pos[0]); // number of element in positions array
// Variables will change:
int lastButtonState2 = HIGH;   // the previous reading from the input pin
int lastButtonState3 = HIGH;   // the previous reading from the input pin
int lastButtonState4 = HIGH;   // the previous reading from the input pin
int oldPos = 10;               // intentional out of range
int slideValue = 0;            // value read from the pot

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
  pinMode(DigitalInPin2, INPUT);
  pinMode(DigitalInPin3, INPUT);
  pinMode(DigitalInPin4, INPUT);
}

void loop() {  
  //read the pushbutton value into a variable
  int DigitalIn2Val = digitalRead(DigitalInPin2);  
  int DigitalIn3Val = digitalRead(DigitalInPin3);  
  int DigitalIn4Val = digitalRead(DigitalInPin4);  
  int posionslide =  positionSlide();
  // if slide or the button state has changed:
  // 1 = button UP , 0 = button DOWN (pressed)
  if (oldPos != posionslide || (DigitalIn2Val != lastButtonState2) || (DigitalIn3Val != lastButtonState3) || (DigitalIn4Val != lastButtonState4)){
    Serial.println(String(positionSlide()) + " " + String(DigitalIn2Val) + " " +  String(DigitalIn3Val) + " " +  String(DigitalIn4Val)); 
    lastButtonState2 = DigitalIn2Val;  
    lastButtonState3 = DigitalIn3Val;  
    lastButtonState4 = DigitalIn4Val;  
    oldPos = posionslide;
  }
  delay(50);                     
}

int positionSlide(){
  // read the analog in value of slide resistors:
  slideValue = analogRead(analogInPin);  
  
  int oldValue =  2000;
  int curpos = 0;
  int diffValue;
   // loop from the lowest value to the highest in the array of positions:
  for (int p = 0; p < posCount ; p++) 
    { 
      diffValue = abs(pos[p] - slideValue);
      if (diffValue < oldValue)
      {
        oldValue = diffValue;
        curpos = p;
      }
  }
  return curpos; 
 
}

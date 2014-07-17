/*Code for the basic attiny45/85 chip with an electret microphone
 */
//                            attiny45/85
//                        reset -+---+- power
//  (on until loud sound)   pb3 -+*  +- pb2 (turns off with sound)
//      | ]-(electret +)    pb4 -+   +- pb1 (turns on with sound)
//      | ]-(electret -) ground -+---+- pb0 (fades on with sound)
// 
// 
// INPORTANT: Connect a ~50k ohm resistor between + lead of electret (pb4) and 
// power, to power the microphone.  The value of this microphone adjusts the 
// sensitivity of the microphone.  The greater the resistor, the more sensitive
// the microphone.  Note, that if the resistor is too large, the microphone will 
// not get enough power (and thus become less sensitive).  
//
// The louder the volume sensed by the electret mic, the higher the 
// voltage read by pb4 (analog input 2).
// Electret mic also works as a wind sensor, so blowing on microphone is 
// equivalent to loud sound.

int fadingLight;
int micPin = 2;

int micSample; // volume picked up by microphone
int maxSample = 0;  // maximum volume for that sample
int totalMaxVolume = 0;  // maximum volume picked up by microphone
int averageVolume = 0;  // average volume for background sound

void setup() {
  pinMode(0, OUTPUT); // fades on with sound
  pinMode(1, OUTPUT); // turns on with sound
  pinMode(2, OUTPUT); // turns off with sound
  pinMode(3, OUTPUT); // on until loud sound 

  digitalWrite(3, HIGH); // start with pin 3 on.  Turns off with lound sound

  //calibrate for average volume by taking 100 samples and averaging
  for( int i=0 ; i< 100; i++)
  {
    micSample = micSample + analogRead(micPin);
  }
  averageVolume = micSample/100;
  averageVolume = averageVolume + 3; // adjust silence threshold by 3.  
  // increase this number (the 2) to make microphone less sensitive to noise.
}


void loop() {
  maxSample = 0;  //reset the maximum volume for this sample

  // take 20 samples of volume and pick the maximum volume
  for( int i=0 ; i< 20; i++) 
  {
    micSample = analogRead(micPin);
    if (micSample > maxSample)
    {
      maxSample= micSample;
    }
  }

  // update maximum volume read by the microphone for calibration
  if (maxSample > totalMaxVolume)
  {
    totalMaxVolume = maxSample;
  }

  // map volume sample to light intensity 
  fadingLight = map(maxSample, averageVolume, totalMaxVolume, 0, 50);
  if(fadingLight<0)  
  {
    fadingLight = 0;
  }
  analogWrite(0, fadingLight);  // write intensity to pin 0
  
  // if volume sample is greater than "loud sound" threshold (in this case 10)
  // then turn off pin 3
  if(maxSample > averageVolume + 10)
  {
    digitalWrite(3, LOW);
  }
  
  // if volume sample is above silence threshold, 
  // turn on pin 1 and turn off pin 2.
  // if voluem sample is below silence threshold, 
  // turn off pin 1 and turn on pin 2.
  if(maxSample > averageVolume)
  {
    digitalWrite(1, HIGH);
    digitalWrite(2, LOW);
  }
  else
  {
    digitalWrite(1, LOW);
    digitalWrite(2, HIGH);
  }
  
  delay(5);
}



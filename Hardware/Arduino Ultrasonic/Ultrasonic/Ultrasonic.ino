#include <Ultrasonic.h>


Ultrasonic ultrasonic(12,13);
void setup() {
Serial.begin(9600);
}
void loop()
{
  Serial.print(ultrasonic.Ranging(CM));
  Serial.println("cm");    
  delay(100);
}

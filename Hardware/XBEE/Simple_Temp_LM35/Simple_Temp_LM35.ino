

float temp;
int tempPin = 0;
int LDR_Pin = A1; //analog pin 0

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // temp
  temp = analogRead(tempPin);
  //temp = temp * 0.48828125;
  temp = temp * 0.4;
  
  Serial.print("Temperature ");
  Serial.println(temp);
  
  // light
  int LDRReading = analogRead(LDR_Pin);
  Serial.print("Light "); 
  Serial.println(1024 - LDRReading);
  
  delay(1000);
}


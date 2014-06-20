int LDR_Pin = A1; //analog pin 0

void setup(){
  Serial.begin(9600);
}

void loop(){
  int LDRReading = analogRead(LDR_Pin); 

  Serial.println(1024 - LDRReading);
  delay(250); //just here to slow down the output for easier reading
}

/**
 *  TV mode Domotics
 *  turn off livingroom lights by IR using NodeMCU 8266 and MCE remote control 
 *  Programmed in Learn Mode to emulate a Majestic IR remote control
 *  More info on how to set MCE Remote  at https://shop.tbsdtv.com/blog/how-to-program-microsoft-mce-remote-control-learning-functionality.html
 *  Created on: 18/10/2017
 *
 */

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>
#define USE_SERIAL Serial

uint16_t RECV_PIN = 14;
IRrecv irrecv(RECV_PIN);
decode_results results;

ESP8266WiFiMulti WiFiMulti;

void setup() {
    USE_SERIAL.begin(115200);
    WiFiMulti.addAP("SSID", "password");
    irrecv.enableIRIn();  // Start the receiver
}

void loop() {
    if (irrecv.decode(&results)) {
      if (results.value == 16713975){
        Serial.println("OK");
        // wait for WiFi connection
        if((WiFiMulti.run() == WL_CONNECTED)) {
            HTTPClient http;
            http.begin("http://192.168.0.202:5000/releoff/5"); //HTTP
            // start connection and send HTTP header
            int httpCode5 = http.GET();
            http.end();
            http.begin("http://192.168.0.202:5000/releoff/1"); //HTTP
            // start connection and send HTTP header
            int httpCode1 = http.GET();
            http.end();
          }
      }
    irrecv.resume();  // Receive the next value
    }
    delay(100);
}

/*
/facedetected/number/name
/shutdown
/reboot
/releoff/number
/releon/number
/reletest
/multireleon/number1/number2/number3/number4/number5
/multireleoff/number1/number2/number3/number4/number5
/reletoggle/number
/reledimmon/number
/reledimmoff/number
/reletimer/number/unlock_after_millisec
/relestate/number
/relestateall
/reletoggle_simply/name
/releofftimer/number/secondi 
 */

#include <SPI.h>
#include <Ethernet.h>
// IR
#include <IRremote.h>

const int pin_sala_1 = 22;   //22  
const int pin_sala_2 = 24;   //24     
const int pin_cucina = 26;   //26       
const int pin_ingresso = 28; //28      
const int pin_dimmer = 30;   //30       
const int pin_porta = 32;    //32       

const int puls_sala_1 = 51; // P3       pin 51  
const int puls_sala_2 = 53; // P4       pin 53  
const int puls_cucina = 47; // P5       pin 47 
const int puls_ingresso = 49; //P2      pin 49 
const int puls_spegni_tutto = 45; // P1 pin 45

const int SHORT_PRESS_TIME = 1000; // 500 milliseconds
unsigned long pressedTime  = 0;
unsigned long releasedTime = 0;

byte mac[] = { 0xBE, 0xAD, 0x0E, 0xEF, 0xFE, 0xEA };   
byte ip[] = { 192, 168, 10, 202 };                      
byte gateway[] = { 192, 168, 10, 1 };                   
byte subnet[] = { 255, 255, 255, 0 };                 
EthernetServer server(5000);                                
String readString;
String versione = "0.4";

// IR
int RECV_PIN = 2;
IRrecv irrecv(RECV_PIN);
decode_results results;

// debouncing
bool old_puls_sala_1 = HIGH;
bool old_puls_sala_2 = HIGH;
bool old_puls_cucina = HIGH;
bool old_puls_ingresso = HIGH;
bool old_puls_spegni_tutto = HIGH;

// memoria stati
bool stato_sala_1  = HIGH;
bool stato_sala_2  = HIGH;
bool stato_cucina = HIGH;
bool stato_ingresso = HIGH;

void setup() {
 // Apro la comunicazione seriale:
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  //Imposto i pin come OUTPUT
  pinMode(pin_sala_1, OUTPUT);
  pinMode(pin_sala_2, OUTPUT);
  pinMode(pin_cucina, OUTPUT);
  pinMode(pin_ingresso, OUTPUT);
  pinMode(pin_dimmer, OUTPUT);
  pinMode(pin_porta, OUTPUT);
  
  digitalWrite(pin_sala_1,stato_sala_1);
  digitalWrite(pin_sala_2,stato_sala_2);
  digitalWrite(pin_cucina,stato_cucina);
  digitalWrite(pin_ingresso,stato_ingresso);
  digitalWrite(pin_dimmer,HIGH);
  digitalWrite(pin_porta,HIGH);

  pinMode(puls_sala_1, INPUT_PULLUP);
  pinMode(puls_sala_2, INPUT_PULLUP);
  pinMode(puls_cucina, INPUT_PULLUP);
  pinMode(puls_ingresso, INPUT_PULLUP);
  pinMode(puls_spegni_tutto, INPUT_PULLUP);

  Ethernet.begin(mac, ip, gateway, subnet);
  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
  Serial.print("server version ");
  Serial.println(versione);

  //IR 
  irrecv.enableIRIn(); // Start the receiver
}

void loop() {

  // IR
  if (irrecv.decode(&results)) {
      Serial.println(results.value);
      if ((results.value == 16713975) || (results.value == 2148500503)){
       ToggleSala();
       delay(500);
      }      
      if ((results.value == 2148467803) || (results.value == 2148500571)) {   // RED
       ToggleIngresso();
       delay(500);
      }
      
      if ((results.value == 2148467804) || (results.value == 2148500572)){   // GREEN
       ToggleCucina();
       delay(500);
      }
      
      if ((results.value == 2148467805) || (results.value == 2148500573)){   // Yellow
       ToggleSalaFull();
       delay(500);
      }
      
      irrecv.resume();  // Receive the next value
    }

// END IR

    
  if ((digitalRead(puls_sala_1) == LOW) && (old_puls_sala_1 == LOW)){
    long pressDuration = millis() - pressedTime;
    if( pressDuration > SHORT_PRESS_TIME ){
      Serial.println("A short press is detected");
      stato_sala_1 = HIGH;
      stato_sala_2 = LOW;
      digitalWrite(pin_sala_1, stato_sala_1);
      digitalWrite(pin_sala_2, stato_sala_2);
    }
    
  }
    
  if ( digitalRead(puls_sala_1) == LOW && old_puls_sala_1 != LOW) {
    pressedTime = millis();
    Serial.println("puls_sala_1");
    stato_sala_1 = !stato_sala_1;
    stato_sala_2 = !stato_sala_1;// sincronizzo gli stati
    digitalWrite(pin_sala_1, stato_sala_1);
    digitalWrite(pin_sala_2, stato_sala_1); // sincronizzo gli stati
    delay(200);
    old_puls_sala_1 = LOW;
  }
  if ( digitalRead(puls_sala_1) == HIGH) old_puls_sala_1 = HIGH;

  
  if ( digitalRead(puls_sala_2) == LOW && old_puls_sala_2 != LOW) {
    Serial.println("puls_sala_2");
    stato_ingresso = !stato_ingresso;
    digitalWrite(pin_ingresso, stato_ingresso);
    delay(200);
    old_puls_sala_2 = LOW;
  }
  if ( digitalRead(puls_sala_2) == HIGH) old_puls_sala_2 = HIGH;
  
  if ( digitalRead(puls_cucina) == LOW && old_puls_cucina != LOW) {
    stato_cucina = !stato_cucina;
    digitalWrite(pin_cucina, stato_cucina);
    delay(200);
    old_puls_cucina = LOW;
  }
  if ( digitalRead(puls_cucina) == HIGH) old_puls_cucina = HIGH;

  if ( digitalRead(puls_ingresso) == LOW && old_puls_ingresso != LOW) {
    stato_ingresso = !stato_ingresso;
    digitalWrite(pin_ingresso, stato_ingresso);
    delay(200);
    old_puls_ingresso = LOW;
  }
  if ( digitalRead(puls_ingresso) == HIGH) old_puls_ingresso = HIGH;

  
  if ( digitalRead(puls_spegni_tutto) == LOW && old_puls_spegni_tutto != LOW) {
    stato_ingresso = HIGH;
    stato_cucina = HIGH;
    stato_sala_1 = HIGH;
    stato_sala_2 = HIGH;
    digitalWrite(pin_ingresso, stato_ingresso);
    digitalWrite(pin_cucina, stato_cucina);
    digitalWrite(pin_sala_1, stato_sala_1);
    digitalWrite(pin_sala_2, stato_sala_2);
    delay(200);
    old_puls_spegni_tutto = LOW;
  }
  if ( digitalRead(puls_spegni_tutto) == HIGH) old_puls_spegni_tutto = HIGH;


  EthernetClient client = server.available();
  if (client) {
    while (client.connected()) {   
      if (client.available()) {
        char c = client.read();
     
        if (readString.length() < 100) {
          //Inserisco i caratteri nella stringa 
          readString += c;
         }

         if (c == '\n') {          
           Serial.println(readString); 
     
           client.println("HTTP/1.1 200 OK"); //Invio nuova pagina
           client.println("Content-Type: text/html");
           client.println();     
           client.println("<HTML>");
           client.println("<HEAD>");
           client.println("<meta name='apple-mobile-web-app-capable' content='yes' />");
           client.println("<meta name='apple-mobile-web-app-status-bar-style' content='black-translucent' />");
           client.println("<link rel='stylesheet' type='text/css' href='http://www.progettiarduino.com/uploads/8/1/0/8/81088074/style3.css' />");
           client.println("<TITLE>DOMOTICS</TITLE>");
           client.println("</HEAD>");
           client.println("<BODY>");
           client.println("<H1>DOMOTICS</H1>");
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/releon/5\"\">Accendi SALA 1</a>");          //Modifica a tuo piacimento:"Accendi LED 5"
           client.println("<a href=\"/releoff/5\"\">Spegni SALA 1</a><br />");    //Modifica a tuo piacimento:"Spegni LED 5"
           client.println("<hr />");
           client.println("<br />");
           client.println("<a href=\"/releon/1\"\">Accendi SALA 2</a>");          //Modifica a tuo piacimento:"Accendi LED 1"
           client.println("<a href=\"/releoff/1\"\">Spegni SALA 2</a><br />");    //Modifica a tuo piacimento:"Spegni LED 1" 
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/releon/4\"\">Accendi CUCINA</a>");          //Modifica a tuo piacimento:"Accendi LED 4"
           client.println("<a href=\"/releoff/4\"\">Spegni CUCINA</a><br />");    //Modifica a tuo piacimento:"Spegni LED 4"
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/releon/3\"\">Accendi INGRESSO</a>");          //Modifica a tuo piacimento:"Accendi LED 3"
           client.println("<a href=\"/releoff/3\"\">Spegni INGRESSO</a><br />");    //Modifica a tuo piacimento:"Spegni LED 3"
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/reletimer/6\"\">DIMMER</a>");          //Modifica a tuo piacimento:"Accendi LED 6"
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/reletimer/8\"\">PORTA</a>");          //Modifica a tuo piacimento:"Accendi LED 6"
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/reletoggle/5\"\">toggle Sala 1</a>");          
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/reletoggle/1\"\">toggle sala 2</a>");            
           client.println("<br />");
           client.println("<br />");
           client.println("<a href=\"/reletoggle/sala\"\">toggle SALA</a>");          
           client.println("<br />");
           client.println("<br />"); 
           client.println("</BODY>");
           client.println("</HTML>");
     
           delay(1);
           client.stop();
           // sala_1
           if (readString.indexOf("/releon/5") >0) {
            stato_sala_1 = LOW;
            digitalWrite(pin_sala_1, stato_sala_1);
           }
           if (readString.indexOf("/releoff/5") >0) {
            stato_sala_1 = HIGH;
            digitalWrite(pin_sala_1, stato_sala_1);
           }
           // sala_2
           if (readString.indexOf("/releon/1") >0) {
            stato_sala_2 = LOW;
            digitalWrite(pin_sala_2, stato_sala_2);
           }
           if (readString.indexOf("/releoff/1") >0) {
            stato_sala_2 = HIGH;
            digitalWrite(pin_sala_2, stato_sala_2);
           }
           // cucina
           if (readString.indexOf("/releon/4") >0) {
            stato_cucina = LOW;
            digitalWrite(pin_cucina, stato_cucina);  
           }
           if (readString.indexOf("/releoff/4") >0) {
            stato_cucina = HIGH;
            digitalWrite(pin_cucina, stato_cucina); 
           }
           // ingresso
           if (readString.indexOf("/releon/3") >0) {
            stato_ingresso = LOW;
            digitalWrite(pin_ingresso, stato_ingresso);  
           }
           if (readString.indexOf("/releoff/3") >0) {
            stato_ingresso = HIGH;
            digitalWrite(pin_ingresso, stato_ingresso);
           }
           // dimmer
           if (readString.indexOf("/reletimer/6") >0){
               digitalWrite(pin_dimmer, LOW);
               delay(1300);
               digitalWrite(pin_dimmer, HIGH);
           }
           // porta
           if (readString.indexOf("/reletimer/8") >0){
               digitalWrite(pin_porta, LOW);
               delay(500);
               digitalWrite(pin_porta, HIGH);
           }
            // toggler
            
           if (readString.indexOf("/reletoggle/5") >0) {
            stato_sala_1 = !stato_sala_1;
            digitalWrite(pin_sala_1, stato_sala_1);
            }
           if (readString.indexOf("/reletoggle/1") >0) {
            stato_sala_2 = !stato_sala_2;
            digitalWrite(pin_sala_2, stato_sala_2);
           }
           if (readString.indexOf("/reletoggle/sala") >0) {
              ToggleSala();
           }
            readString="";  
          }
         }
       }
    }
    
}

void ToggleSala(){
        // case provious ON
      if ((stato_sala_1 == LOW ) || ( (stato_sala_2 == LOW ))){
        stato_sala_1 = HIGH;
        stato_sala_2 = HIGH;
      digitalWrite(pin_sala_1, stato_sala_1);
      digitalWrite(pin_sala_2, stato_sala_2);
     }
     else{
        //stato_sala_1 = LOW;
        stato_sala_2 = LOW;
      //digitalWrite(pin_sala_1, stato_sala_1);
      digitalWrite(pin_sala_2, stato_sala_2);
      
     }
  }
  
void ToggleSalaFull(){
        // case provious ON
      if ((stato_sala_1 == LOW ) || ( (stato_sala_2 == LOW ))){
        stato_sala_1 = HIGH;
        stato_sala_2 = HIGH;
      digitalWrite(pin_sala_1, stato_sala_1);
      digitalWrite(pin_sala_2, stato_sala_2);
     }
     else{
        stato_sala_1 = LOW;
        stato_sala_2 = LOW;
      digitalWrite(pin_sala_1, stato_sala_1);
      digitalWrite(pin_sala_2, stato_sala_2);
      
     }
  }

void ToggleIngresso(){
        // case provious ON
      if (stato_ingresso == LOW ){
        stato_ingresso = HIGH;
      digitalWrite(pin_ingresso, stato_ingresso);
     }
     else{
        stato_ingresso = LOW;
      digitalWrite(pin_ingresso, stato_ingresso);
      
     }
  }
void ToggleCucina(){
        // case provious ON
      if (stato_cucina == LOW ){
        stato_cucina = HIGH;
      digitalWrite(pin_cucina, stato_cucina);
     }
     else{
        stato_cucina = LOW;
      digitalWrite(pin_cucina, stato_cucina);
      
     }
  }

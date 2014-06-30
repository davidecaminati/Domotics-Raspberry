#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>

//Librerie impiegate per il progetto
#include <SPI.h>
#include <Ethernet.h>
 
//Creao un array di byte per specificare il mac address
byte mac[] = { 0x50, 0xCC, 0xF8, 0x57, 0x96, 0x2D };
//creo un array di byte per specificare l'indirizzo ip
byte ip[] = {192, 168, 0, 252};
 
//creo una variabile char per memorizzare i byte letti dal client
char Data_RX;
 
//creao un oggetto server che rimane in ascolto sulla porta
//specificata
EthernetServer ArduinoServer(80);
 
void setup()
{
    //inizializza lo shield con il mac e l'ip
    Ethernet.begin(mac, ip);
    //inizializza l'oggetto server
    ArduinoServer.begin();
    Serial.begin(9600); 
    Serial.println("ciao");
}
 
void loop()
{
     //Ascolto le richieste dei client controllo se ci sono dati da leggere
     //e creo un oggetto relativo a client che sta interrogando l'Ethernet shield
     EthernetClient  pc_client = ArduinoServer.available();
     //controllo se pc_client è true
if (pc_client)
   {
       //controllo continuamente che il client sia connesso
       while (pc_client.connected())
       {
           //Controllo se ci sono byte disponibili per la lettura
           if (pc_client.available())
           {
               //leggo i byte disponibili
               //provenienti dal client
               Data_RX = pc_client.read();
 
               //Attendo che tutti i byte siano letti
               //quando Data_RX contiene il carattere
               //di nuova line capisco tutti i byte sono
               //stati letti
               if (Data_RX == '\n')
               {
                   //Invio la risposta al client
                   //invio lo status code
                   pc_client.println("HTTP/1.1 200 OK");
                   //imposto il data type
                   pc_client.println("Content-Type: text/html");
                   pc_client.println();
                   //invio codice html
                   pc_client.print("<html><body><h1>");
                   pc_client.print("Hello world Arduino Web Server</h1></body></html>");
                   //aspetto 1 ms affinche la risposta giunga al browser del client
                   delay(1);
                   //esco dal ciclo while una volta completato l'invio della risposta
                   break;
               }
           }
       }
       //chiudo la connessione
       pc_client.stop();
   }
}

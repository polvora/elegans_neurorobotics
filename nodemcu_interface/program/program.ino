#include <Servo.h>
#include <ESP8266WiFi.h>


// Routing Motor Board to NodeMCU GPIO
static const uint8_t MB_D0   = 16;   // GPIO_16
static const uint8_t MB_D1   = 5;    // GPIO_05
static const uint8_t MB_D2   = 4;    // GPIO_04
static const uint8_t MB_D3   = 0;    // GPIO_00
static const uint8_t MB_D4   = 2;    // GPIO_02
static const uint8_t MB_D5   = 14;   // GPIO_14
static const uint8_t MB_D6   = 12;   // GPIO_12
static const uint8_t MB_D7   = 13;   // GPIO_13 - RX2
static const uint8_t MB_D8   = 15;   // GPIO_15 - TX2
static const uint8_t MB_D9   = 3;    // GPIO_03 - RX0
static const uint8_t MB_D10  = 1;    // GPIO_01 - TX0
static const uint8_t MB_SD2  = 9;    // GPIO_09
static const uint8_t MB_SD3  = 10;   // GPIO_10

Servo Axis0;
Servo Axis1;  
Servo Axis2;  
Servo Axis3;  
Servo Axis4;
Servo Axis5;
Servo Axis6;
Servo Axis7;
Servo Axis8;

char* ssid = "GPT";
const char* password = "otrotipoA1";

const uint16_t port = 9000;
const char * host = "192.168.0.17";

void setup() {
  Axis0.attach(MB_D0);
  Axis1.attach(MB_D1);
  Axis2.attach(MB_D2);
  Axis3.attach(MB_D3);
  Axis4.attach(MB_D4);
  Axis5.attach(MB_D5);
  Axis6.attach(MB_D6);
  Axis7.attach(MB_D7);
  Axis8.attach(MB_D8);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void loop() {

  WiFiClient client;
  if (!client.connect(host, port)) {
      delay(1000);
      return;
  }

  while (client.connected()) {
    Axis0.write(90);
    Axis1.write(90);
    Axis2.write(90);
    Axis3.write(90);
    Axis4.write(90);
    Axis5.write(90);
    Axis6.write(90);
    Axis7.write(90);
    Axis8.write(90);
    client.println("hello from ESP8266");
  }
  client.stop();
}


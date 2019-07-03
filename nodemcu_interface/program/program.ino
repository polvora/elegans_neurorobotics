#include <Servo.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>

// Routing motor board pins to NodeMCU GPIO
#define M0 16    // GPIO_16
#define M1 5     // GPIO_05
#define M2 4     // GPIO_04
#define M3 0     // GPIO_00
#define M4 2     // GPIO_02
#define M5 14    // GPIO_14
#define M6 12    // GPIO_12
#define M7 13    // GPIO_13 - RX2
#define M8 15    // GPIO_15 - TX2

// ADCs (I2C Communication)
#define SCL 3     // Redefine default SCL to RX0 pin
#define SDA 1     // Redefine default SDA to TX0 pin
#define I2C_MASTER 0x08
#define ADC_ADDR0 0x48
#define ADC_ADDR1 0x49
#define ADC_ADDR2 0x4A
#define ADC_ADDR3 0x4B

// Servos
Servo Axis0;
Servo Axis1;  
Servo Axis2;  
Servo Axis3;  
Servo Axis4;
Servo Axis5;
Servo Axis6;
Servo Axis7;
Servo Axis8;

long angle0, angle1, angle2, angle3, angle4, angle5, angle6, angle7, angle8;

// ADCs
Adafruit_ADS1115 ADC0(ADC_ADDR0);
Adafruit_ADS1115 ADC1(ADC_ADDR1);
Adafruit_ADS1115 ADC2(ADC_ADDR2);
Adafruit_ADS1115 ADC3(ADC_ADDR3);

uint16_t SL0, SL1, SL2, SL3, SL4, SL5, SL6, SL7;
uint16_t SR0, SR1, SR2, SR3, SR4, SR5, SR6, SR7;

char* ssid = "GPT";
const char* password = "otrotipoA1";

const uint16_t port = 5000;
const char * host = "192.168.0.17";

String sentMessage = "";
String receivedMessage = "";
char receivedChar = 0;

void setup() {
  // Assigns Digital outputs to each axis
  Axis0.attach(M0);
  Axis1.attach(M1);
  Axis2.attach(M2);
  Axis3.attach(M3);
  Axis4.attach(M4);
  Axis5.attach(M5);
  Axis6.attach(M6);
  Axis7.attach(M7);
  Axis8.attach(M8);

  Wire.begin(SDA, SCL); // Start communication with ADCs
  // Gain set the FSR to +/- 4.096V and LSB to 125 μV, see ADS1115 datasheet for more gains
  // As VDD voltage is 3.3V the analog read never reaches the full range (4V)
  ADC0.setGain(GAIN_ONE); // Gain multiplier (x1)
  
  WiFi.mode(WIFI_STA); // WiFi Mode Station (not broadcasting)
  WiFi.begin(ssid, password); // Connect to WiFi Acces Point
  while (WiFi.status() != WL_CONNECTED) { // Waits till connected
    delay(500);
  }
  
  // Centers all axis 
  Axis0.write(90);
  Axis1.write(90);
  Axis2.write(90);
  Axis3.write(90);
  Axis4.write(90);
  Axis5.write(90);
  Axis6.write(90);
  Axis7.write(90);
  Axis8.write(90);
}

void loop() {
  WiFiClient client; // Creates raw client socket
  if (!client.connect(host, port)) { // Connects to server
      delay(1000); // Retries after 1 sec
      return;
  }
  // Work while connected
  while (client.connected()) { 
    // Analog sensors read
    SL0 = ADC0.readADC_SingleEnded(0);
    SL1 = ADC0.readADC_SingleEnded(1);
    SL2 = ADC0.readADC_SingleEnded(2);
    SL3 = ADC0.readADC_SingleEnded(3);
    // Data packaging 
    sentMessage = "SL0: " + String(SL0, DEC) + " ; ";
    sentMessage += "SL1: " + String(SL1, DEC) + " ; ";
    sentMessage += "SL2: " + String(SL2, DEC) + " ; ";
    sentMessage += "SL3: " + String(SL3, DEC) + " ; "; 
    sentMessage += "SL4: " + String(SL4, DEC) + " ; "; 
    sentMessage += "SL5: " + String(SL5, DEC) + " ; "; 
    sentMessage += "SL6: " + String(SL6, DEC) + " ; "; 
    sentMessage += "SL7: " + String(SL7, DEC) + " ; "; 
    sentMessage += "SR0: " + String(SR0, DEC) + " ; "; 
    sentMessage += "SR1: " + String(SR1, DEC) + " ; ";
    sentMessage += "SR2: " + String(SR2, DEC) + " ; ";
    sentMessage += "SR3: " + String(SR3, DEC) + " ; ";
    sentMessage += "SR4: " + String(SR4, DEC) + " ; ";
    sentMessage += "SR5: " + String(SR5, DEC) + " ; ";
    sentMessage += "SR6: " + String(SR6, DEC) + " ; ";
    sentMessage += "SR7: " + String(SR7, DEC) + " ; ";
    client.println(sentMessage);
    
    receivedMessage = "";
    while (client.available()) {
      receivedChar = client.read();
      
      if (receivedChar == '\n') { // New line is the end of the message 
        // Extracts each axis angle from the message string
        angle0 = receivedMessage.substring((receivedMessage.indexOf("AX0: ")+5), receivedMessage.indexOf(" ; AX1")).toInt();
        angle1 = receivedMessage.substring((receivedMessage.indexOf("AX1: ")+5), receivedMessage.indexOf(" ; AX2")).toInt();
        angle2 = receivedMessage.substring((receivedMessage.indexOf("AX2: ")+5), receivedMessage.indexOf(" ; AX3")).toInt();
        angle3 = receivedMessage.substring((receivedMessage.indexOf("AX3: ")+5), receivedMessage.indexOf(" ; AX4")).toInt();
        angle4 = receivedMessage.substring((receivedMessage.indexOf("AX4: ")+5), receivedMessage.indexOf(" ; AX5")).toInt();
        angle5 = receivedMessage.substring((receivedMessage.indexOf("AX5: ")+5), receivedMessage.indexOf(" ; AX6")).toInt();
        angle6 = receivedMessage.substring((receivedMessage.indexOf("AX6: ")+5), receivedMessage.indexOf(" ; AX7")).toInt();
        angle7 = receivedMessage.substring((receivedMessage.indexOf("AX7: ")+5), receivedMessage.indexOf(" ; AX8")).toInt();
        angle8 = receivedMessage.substring((receivedMessage.indexOf("AX8: ")+5), receivedMessage.lastIndexOf(" ;")).toInt();
        
        Axis0.write(angle0);
        Axis1.write(angle1);
        Axis2.write(angle2);
        Axis3.write(angle3);
        Axis4.write(angle4);
        Axis5.write(angle5);
        Axis6.write(angle6);
        Axis7.write(angle7);
        Axis8.write(angle8);
      }
      else { // Message keeps going
        receivedMessage += receivedChar;
      }
    }
    delay(100);
  }
  client.stop();
}


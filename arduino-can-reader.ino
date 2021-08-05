#include <SPI.h>
#include "mcp_can.h"

///////////////////
// Configuration //
///////////////////

// CS pin for CAN bus shield.
// The default pin depends on the shield's version:
//  - 1.0: digital pin 10
//  - 1.1 and newer: digital pin 9
const int CS_PIN = 10;
long unsigned int id;
// Serial port data rate
const long SERIAL_SPEED = 115200;

// CAN bus data rate
const byte CAN_SPEED = CAN_125KBPS;
#define CAN0_INT 2  
///////////////////

MCP_CAN CAN(CS_PIN);
unsigned char len = 0;
byte buffer[8];

void setup() {
    Serial.begin(SERIAL_SPEED);
    byte canSpeed = CAN_SPEED;

  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
    pinMode(CAN0_INT, INPUT);
    // Configuring pin for /INT input
          Serial.println("FRAME:ID=246:LEN=8:8E:62:1C:F6:1E:63:63:20");

  }
}

void loop() {
            Serial.println("FRAME:ID=246:LEN=8:8E:62:1C:F6:1E:63:63:20");
    if (CAN.checkReceive() == CAN_MSGAVAIL) {
        //
        CAN.readMsgBuf(&id, &len, buffer);
        //^^^^^pas bon, n'importe quoi ! d'où ça sort !!
        
        //CAN.readMsgBuf(&len, buffer);
        //int id = CAN.getCanId();
        
        //supprimer mon define de l'ID dans l'init
        
        
        Serial.print("FRAME:ID=");
        Serial.print(id);
        Serial.print(":LEN=");
        Serial.print(len);
        
        char tmp[3];
        for(int i = 0; i<len; i++) {
            Serial.print(":");
            
            snprintf(tmp, 3, "%02X", buffer[i]);
            
            Serial.print(tmp);
        }

        Serial.println();
    }
}

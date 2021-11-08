#include <SPI.h>
#include "mcp_can.h"

///////////////////
// Configuration //
///////////////////

// CS pin for CAN bus shield.
const int CS_PIN = 10;
MCP_CAN CAN(CS_PIN);

// Serial port data rate
const long SERIAL_SPEED = 115200;

// CAN bus data rate
const byte CAN_SPEED = CAN_125KBPS;

byte data = 0x00;
///////////////////


void setup() {
  Serial.begin(SERIAL_SPEED);
  byte canSpeed = CAN_SPEED;
  
  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
    
  }
}


void loop() {
    Serial.println("Press Enter ..."); 
    while (Serial.available() == 0) {
    // Wait for User to Input Data
    delay(50);
    }

    if (Serial.readString() != 10){
      data++;
      Serial.println(data);  
      byte infomsg[] = {0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
      CAN.sendMsgBuf(417, 0, 8, infomsg);
  }
}

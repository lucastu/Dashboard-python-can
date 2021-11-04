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
///////////////////

unsigned long lastCDCactivation =0;

void setup() {
  Serial.begin(SERIAL_SPEED);
  byte canSpeed = CAN_SPEED;
  
  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
  }
}


void loop() {
      Serial.println(millis()-lastCDCactivation);
      if (millis()-lastCDCactivation >=100){
        byte dataInit[] = {0x20, 0x01, 0x06, 0x05, 0x00, 0x08, 0x00};
        CAN.sendMsgBuf(354, 0, 7, dataInit);
        byte dataInit2[] = {0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00};
        CAN.sendMsgBuf(482, 0, 7, dataInit2);
        lastCDCactivation = millis();
        Serial.println("Data sent");
      }
}

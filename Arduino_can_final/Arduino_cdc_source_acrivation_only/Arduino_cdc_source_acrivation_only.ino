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
#define CAN0_INT 2  
///////////////////


void setup() {
  Serial.begin(SERIAL_SPEED);
  byte canSpeed = CAN_SPEED;
  
  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
    pinMode(CAN0_INT, INPUT);
  }
}


void loop() {
      //byte dataInit[] = {0x20, 0x01, 0x06, 0x05, 0x00, 0x10, 0x00};
      byte dataInit[] = {0x00, 0x00, 0x06, 0x05, 0x01, 0x06, 0x00};
      CAN.sendMsgBuf(354, 0, 7, dataInit);
      delay(100);
} 

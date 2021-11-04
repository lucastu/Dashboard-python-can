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
    pinMode(CAN0_INT, INPUT);

  }
  // autowp.github.io/#39B
  //2021 Novembre 4 00:00
  byte datadate[] = {0x95, 0x0b, 0x04, 0x00, 0x00};
  CAN.sendMsgBuf(859, 0, 5, datadate);
}


void loop() {
      delay(1000000);
      }

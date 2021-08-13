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
    // Si on est ok envoi de la trame check
    Serial.println("FRAME:ID=0:LEN=8:00:00:00:00:00:00:00:00");

  }
}


void loop() {
Serial.println("FRAME:ID=1:LEN=1:02");
Serial.println("FRAME:ID=2:LEN=1:10");
Serial.println("FRAME:ID=3:LEN=1:01");
Serial.println("FRAME:ID=4:LEN=8:20:43:55:4C:54:55:52:45");
Serial.println("FRAME:ID=5:LEN=2:03:92");
Serial.println("FRAME:ID=6:LEN=1:02");
Serial.println("FRAME:ID=8:LEN=8:7F:FF:00:FF:FF:FF:FF:FF");
Serial.println("FRAME:ID=9:LEN=2:7F:FF");
Serial.println("FRAME:ID=12:LEN=7:35:07:70:00:3D:08:62");
Serial.println("FRAME:ID=13:LEN=7:41:27:0F:00:4C:23:CE");
Serial.println("FRAME:ID=14:LEN=7:00:FF:FF:03:34:FF:FF");
Serial.println("FRAME:ID=16:LEN=7:00:00:00:3F:00:00:0B");

    delay(1000000);  
} 
    

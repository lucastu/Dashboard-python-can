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

typedef enum {
  INFO_MSG_FRAME       = 0x08,
} FrameType;

// Information message data (automatic wipers, open door, ...)
byte messageInfo[8];

void setup() {
  Serial.begin(SERIAL_SPEED);
  byte canSpeed = CAN_SPEED;
  
  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
    pinMode(CAN0_INT, INPUT);
  }
}


void loop() {
  
  unsigned char len = 0;
  byte buffer[8];
  byte tmp[9];
  int tempValue;
  long unsigned int id;
  
  if (CAN.checkReceive() == CAN_MSGAVAIL) {
    CAN.readMsgBuf(&id, &len, buffer);

      if (id == 417) {
      // Information message frame
      // We send the raw frame over serial as there is many different data
      // to parse in it, so we do it on the iOS app side
      for (int i = 0; i < len; ++i) {
        tempBuffer[i] = buffer[i];
      }
      
      if (memcmp(tempBuffer, messageInfo, 8)) {
        memcpy(messageInfo, tempBuffer, 8);
        
        sendFrameWithType(INFO_MSG_FRAME, messageInfo, 8);
      }
    }

} 
    
    //Fonction d'envoi du message à la raspberry
    void sendFrameWithType( long unsigned int id,  byte data[] , int len) {
      //byte data[] = { 0x12, 0xF0, 0x0F, 0x11 };
      Serial.print("FRAME:ID=");
      Serial.print(id);
      Serial.print(":LEN=");
      Serial.print(len);  
      char tmp[3];
      for(int i = 0; i<len; i++) {
        Serial.print(":");
        snprintf(tmp, 3, "%02X", data[i]);   
        Serial.print(tmp);
      }
      Serial.println();   
    }  
    
    inline void sendByteWithType( long unsigned int frameType,  byte byteToSend[]) {
      //on crée un tableau du byte du buffer
      byte arr[] = { byteToSend };
      sendFrameWithType(frameType, arr, 1);
    }  

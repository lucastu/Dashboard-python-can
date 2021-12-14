#include <SPI.h>
#include "mcp_can.h"

///////////////////
// Configuration //
///////////////////

// CS pin for CAN bus shield.
const int CS_PIN = 10;
MCP_CAN CAN(CS_PIN);

//Pin of car radio power state
const int Radio_POWER_PIN = 3;

//Pin to control power relay
const int Relay_PIN = 4;

// LCD power switch pin
const int screenBrightnessPin = 6;
const int screenPowerPin = 7;

// Serial port data rate
const long SERIAL_SPEED = 115200;

// CAN bus data rate
const byte CAN_SPEED = CAN_125KBPS;
#define CAN0_INT 2  
///////////////////

typedef enum {
  INIT_STATUS_FRAME    = 0x00,
  VOLUME_FRAME         = 0x01,
  TEMPERATURE_FRAME    = 0x02,
  RADIO_SOURCE_FRAME   = 0x03,
  RADIO_NAME_FRAME     = 0x04,
  RADIO_FREQ_FRAME     = 0x05,
  RADIO_FMTYPE_FRAME   = 0x06,
  RADIO_DESC_FRAME     = 0x07,
  INFO_MSG_FRAME       = 0x08,
  RADIO_STATIONS_FRAME = 0x09,
  INFO_TRIP_FRAME      = 0x0C,
  INFO_INSTANT_FRAME   = 0x0E,
  //TRIP_MODE_FRAME      = 0x0F,
  AUDIO_SETTINGS_FRAME = 0x10,
  REMOTE_COMMAND_FRAME = 0x11,
  OPEN_DOOR_FRAME      = 0x12,
  SHUTDOWN_FRAME       = 0x14,
} FrameType;

///////////////////////
// Variables tampons //
///////////////////////
// Radio volume
int volume = 0;

// Outside temperature
int temperature = 0;

// Radio source (FM, AUX1, AUX2, ...)
int radioSource = 0;

// FM band number (1, 2, AST)
int fmType = 0;

// Radio frequency
int fmFreq = 0;

// Radio station name
char radioName[9];

// Radio text
char radioMsg[100];
char msgRecvCount = 0;

// Saved stations
char stations[100];
char stationsRecvCount = 0;
char tempBuffer[100];

// Steering wheel button 
byte remotecommand = 0;

// Open doors 
byte opendoors = 0;

// Information message data (automatic wipers, open door, ...)
byte messageInfo[8];

// Audio settings (bass/treble, equalizer, ...)
byte audioSettings[7];

// Trip computer data (memory 1, memory 2, instant data)
byte infoTrip1[7];
byte infoInstant[7];


// Keeping time since la frame was sent to radio
unsigned long lastCDCactivation =0;

void setup() {
  Serial.begin(SERIAL_SPEED);
  byte canSpeed = CAN_SPEED;
  
  //Input for monitoring 
  pinMode(Radio_POWER_PIN , INPUT_PULLUP);  
  //Put the pin in INPUT mode correspond to HI-Z mode
  pinMode(screenBrightnessPin, INPUT);
  
  pinMode(Relay_PIN, OUTPUT);
  digitalWrite(Relay_PIN, HIGH);
  
  if (CAN.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) {
    CAN.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.
    pinMode(CAN0_INT, INPUT);
    Serial.println("FRAME:ID=0:LEN=8:00:00:00:00:00:00:00:00");     // If everything good, send this init OK frame
  }
}

void loop() {
  unsigned char len = 0;
  byte buffer[8];
  byte tmp[9];
  int tempValue;
  long unsigned int id;
  
  // Send two msgs to the RD4 every 100ms to activate CDcharger Source
  if (millis()-lastCDCactivation >=100){
      byte dataInitCDC[] = {0x20, 0x01, 0x06, 0x05, 0x00, 0x08, 0x00};
      byte dataInitCDC2[] = {0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00};
      CAN.sendMsgBuf(354, 0, 7, dataInitCDC);
      CAN.sendMsgBuf(482, 0, 7, dataInitCDC2);
      lastCDCactivation = millis();
  }
  
  // If power of radio off, shutdown raspberry 
  // Wait and resend shutdown frame for security
  // If I find a way : check state of raspberry to be sure that it's down before shutoff
  if (digitalRead(Radio_POWER_PIN ) == LOW)  {
    sendByteWithType(SHUTDOWN_FRAME, 0x01);
    delay(10000);
    sendByteWithType(SHUTDOWN_FRAME, 0x01);  
    delay(10000);
    sendByteWithType(SHUTDOWN_FRAME, 0x01);  
    delay(2000);
    digitalWrite(Relay_PIN, LOW);
  }
  
  // If a msg is available from canbus
  if (CAN.checkReceive() == CAN_MSGAVAIL) {
    CAN.readMsgBuf(&id, &len, buffer);
    
    if (id==421) {
      // Volume
      tempValue = buffer[0];
      if (volume != tempValue) {
        volume = tempValue;
        sendByteWithType(VOLUME_FRAME, volume);    
      }  
    }else if (id == 246 && len == 8) {
      tempValue = ceil((buffer[5] & 0xFF) / 2.0) - 40;
      if (temperature != tempValue) {
          temperature = tempValue;
          sendByteWithType(TEMPERATURE_FRAME, temperature);
      }
    }else if (id == 543) {
      // Steering wheel button command
      tempValue = buffer[0];
      if (remotecommand != tempValue) { 
        remotecommand = tempValue;
        sendByteWithType(REMOTE_COMMAND_FRAME, remotecommand); 
      }
    } else if (id == 997) {
      // Radio face button
      // Replicate dark button press to the screen button
       if ((buffer[2] & 0b00000100) == 0b00000100) {
         //Put the pin in OUTPUT mode and LOW to simulate the press
         pinMode(screenBrightnessPin, OUTPUT);
         digitalWrite(screenBrightnessPin, LOW);
       }
       else {
         //Put the pin in INPUT mode correspond to HI-Z mode
         pinMode(screenBrightnessPin, INPUT);
       } 
      
    } else if (id == 544) {
      // Openned doors
      tempValue = buffer[0];
      if (opendoors != tempValue) { 
        opendoors = tempValue;
        sendByteWithType(OPEN_DOOR_FRAME, opendoors); 
      }
    } else if (id == 357) {
      //Radio display on or off
       if ((buffer[0] & 0b10000000) == 0b10000000) {digitalWrite(screenPowerPin, HIGH);}
       else {digitalWrite(screenPowerPin, LOW);}      
      
      // Radio source
      tempValue = buffer[2] >> 4;
      if (radioSource != tempValue) { 
        radioSource = tempValue;
        sendByteWithType(RADIO_SOURCE_FRAME, radioSource); 
      }
    } else if (id == 677) {
      // Radio station name
      if (strncmp((char*)buffer, radioName, len)) {
        strncpy(radioName, (char*)buffer, len);
        sendFrameWithType(RADIO_NAME_FRAME, buffer, len); 
      }    
    }else if (id == 549) {
      // Radio frequency
      tempValue = ((((buffer[3] & 0xFF) << 8) + (buffer[4] & 0xFF)) / 2 + 500);
      if (fmFreq != tempValue) {
        fmFreq = tempValue;
        
        byte freqBytes[] = { (fmFreq >> 8) & 0xFF, fmFreq & 0xFF };
        sendFrameWithType(RADIO_FREQ_FRAME, freqBytes, 2);
      }
      
      // FM type
      tempValue = buffer[2] >> 4;
      if (fmType != tempValue) {
        fmType = tempValue;
        
        sendByteWithType(RADIO_FMTYPE_FRAME, fmType);
      }
    }else if (id == 164) {
      // Radio text frame
      
      // This frame can have different meanings depending on its first byte
      // When the radio receive a message from RDS, it will send a frame
      // where the first byte is 0x10 and the two last bytes contains the first 2
      // characters of the message.
      // We send need to send CAN frame 159 with [0x30, 0x00, 0x0A] to receive the
      // remaining data
      // The radio will then send numbered frames containing the remaining text
      // (from 0x20 to 0x29). We have to be careful as they are not always received
      // in the right order, so we have to fill the radioMsg array according to the
      // frame "index". When we received 10 frames, the text is complete and we can
      // send it over serial. If the radio stops sending the text for a any reason,
      // it will send a frame with its first byte set to 0x05 to "reset" the counter
      // so we can receive a full frame next time.
      
      if (buffer[0] == 0x05) {
        msgRecvCount = 0;
      }
      
      if (buffer[0] & 0x10) {
        msgRecvCount++;
        
        radioMsg[0] = buffer[6];
        radioMsg[1] = buffer[7];
        
        byte data[] = { 0x30, 0x00, 0x0A };
        CAN.sendMsgBuf(159, 0, 3, data);
      } else if (buffer[0] & 0x20) {
        msgRecvCount++;
        
        int idx = buffer[0] & 0x0F;
        for (int i = 1; i < len; i++) {
          radioMsg[2 + (idx - 1) * 7 + (i - 1)] = buffer[i];
        }
        
        if (buffer[0] == 0x29) {
          radioMsg[2 + (idx - 1) * 7 + (len - 1)] = '\0';
        }
      }
      
      if (msgRecvCount == 10) {
        sendFrameWithType(RADIO_DESC_FRAME, (byte*)radioMsg, strlen(radioMsg));
        msgRecvCount = 0;
      }
    } else if (id == 293) {
      // Memorized radio station names. Works roughly the same way as frame 164
      // (see above)
      if (buffer[0] & 0x10) {
        stationsRecvCount = 0;
        
        tempBuffer[0] = buffer[6];
        tempBuffer[1] = buffer[7];
      } else if (buffer[0] & 0x20) {
        stationsRecvCount++;
        
        int idx = buffer[0] & 0x0F;
        for (int i = 1; i < len; i++) {
          tempBuffer[2 + (idx - 1) * 7 + (i - 1)] = buffer[i];
        }
        
        if (buffer[0] == 0x29) {
          tempBuffer[2 + (idx - 1) * 7 + (len - 1)] = '\0';
        }
      }
      
      if (stationsRecvCount == 8) {
        char* p = tempBuffer;
        while (*p != '\0') {
          if (*p == '\xA0' || *p == '\xB0' || *p == '\x90' || *p > 127) {
            // set separator between station names
            *p = '|';
          }
          
          p++;
        }
        
        if (strcmp(tempBuffer, stations)) {
          strcpy(stations, tempBuffer);
          
          sendFrameWithType(RADIO_STATIONS_FRAME, (byte*)stations, strlen(stations));
        }
        stationsRecvCount = 0;
      }
    } else if (id == 417) {
      // Information message frame
      // We send the raw frame over serial as there is many different data
      // to parse in it, so we do it on the raspberry side
      for (int i = 0; i < len; ++i) {
        tempBuffer[i] = buffer[i];
      }
      
      if (memcmp(tempBuffer, messageInfo, 8)) {
        memcpy(messageInfo, tempBuffer, 8);
        
        sendFrameWithType(INFO_MSG_FRAME, messageInfo, 8);
      }
    } else if (id == 673 || id == 545) {
      // Trip computer data frames
      // There is 2 different frames (1 for each data set)
      // but they're all structured the same way
      byte* value;
      byte frameType;
      
      switch (id) {
        case 673:
        value = infoTrip1;
        frameType = INFO_TRIP_FRAME;
        break;
          
        case 545:
        value = infoInstant;
        frameType = INFO_INSTANT_FRAME;
        break;
      }
      
      if (memcmp(buffer, value, 7)) {
        memcpy(value, buffer, 7);
        
        sendFrameWithType(frameType, value, 7);
      }
    } else if (id == 485) {
        // Audio settings frame
        // Same as information message frame: we send the raw frame and parse it in the raspberry
        for (int i = 0; i < 7; ++i) {
          tempBuffer[i] = buffer[i];
        }
        
        if (memcmp(tempBuffer, audioSettings, 7)) {
           memcpy(audioSettings, tempBuffer, 7);
           sendFrameWithType(AUDIO_SETTINGS_FRAME, audioSettings, 7);
        }
      }
    }
} 
    
//Function that sends the data to the raspberry
void sendFrameWithType( long unsigned int id,  byte data[] , int len) {
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
  //Make an array from the byte 
  byte arr[] = { byteToSend };
  sendFrameWithType(frameType, arr, 1);
}  

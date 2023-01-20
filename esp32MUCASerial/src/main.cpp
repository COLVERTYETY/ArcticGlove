#include <Muca.h>
#include <Arduino.h>
#define DEBUG

Muca muca;

bool sync_state = 0;

int last_sync = 0;

int sync_timeout = 1000;

void setup() {
  Serial.begin(250000);
#ifdef DEBUG
  Serial.println("Initializing...");
#endif
  muca.init(false);
#ifdef DEBUG

  Serial.print("Chip ID : ");
  Serial.println(muca.getRegister(0xA3));
  Serial.print("FW Library Version : ");
  Serial.println(muca.getRegister(0xA1) << 8 | muca.getRegister(0xA2));
  Serial.print("Firmware ID : ");
  Serial.println(muca.getRegister(0xA6));
#endif  
  //muca.printAllRegisters();
  muca.useRawData(true); // If you use the raw data mode, the interrupt will not work
  
  muca.setGain(31);
  
  // Custom panels :
  // Put a "0" when physical rx or tx line is not connected, "1" instead
  bool rx[]={1,1,1,1,1,1,1,1,1,1,1,1};
  bool tx[]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
  muca.selectLines(rx, tx); // Comment this line to use the full panel
#ifdef DEBUG
  Serial.print("Num_TX/Rows : ");
  Serial.println(muca.num_TX);
  Serial.print("Num_RX/Columns: ");
  Serial.println(muca.num_RX);
  // muca.grid[] is now num_TX * num_RX in size
#endif

}

void loop() {

if (sync_state == 0) {
      while(!Serial.available()) {  // Sync
      Serial.print("RX:");Serial.print(muca.num_RX);Serial.print(":TX:");Serial.print(muca.num_TX);Serial.println(":SYNC");
      delay(500);
    }
    Serial.read();
    sync_state = 1;
  }


  if (muca.update()) {
    for (int i = 0; i < muca.num_TX * muca.num_RX; i++) {
      Serial.print(muca.grid[i]);
      if (i != muca.num_TX * muca.num_RX - 1)
        Serial.print(",");
    }
    Serial.println();
    while(!Serial.available()){
      if (millis() - last_sync > sync_timeout) {
        sync_state = 0;
        last_sync = millis();
        break;
      }
    }
    Serial.read();
    //if(muca.num_RX*muca.num_TX < 150) {
     delay(16);    // Needed if panel size is small
    //}
  }
}
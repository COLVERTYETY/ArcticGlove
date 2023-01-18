

#include "Muca.h"
#include <Arduino.h>


Muca muca;

void SendRawByte();
void SendRawString();

bool led_state = false;


#define rstpin 2

char buffer[10];
// bool led_status = false;

void setup() {
  Serial.begin(250000);
 // muca.skipLine(TX, (const short[]) { 1, 2, 3, 4 }, 4);
  //muca.skipLine(TX, (const short[]) { 14,15,16,17, 18, 19, 20, 21 }, 8);
  // muca.skipLine(RX,(const short[]) {11,12}, 2);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(rstpin, OUTPUT);
  digitalWrite(rstpin, HIGH);
  muca.init();
  muca.useRawData(true); // If you use the raw data, the interrupt is not working

  delay(50);
  muca.setGain(45);

}

void loop() {
  if (muca.updated()) {
    SendRawString();
    //  SendRawByte(); // Faster
    led_state = !led_state;
    digitalWrite(LED_BUILTIN, led_state);
  }else{
    Serial.println("no update");
  }
  // SendRawString();
  delay(20); // waiting 16ms for 60fps
  // Serial.println("reset");s

}



void SendRawString() {
  // Print the array value
  Serial.print("/");
  for (int i = 0; i < NUM_ROWS * NUM_COLUMNS ; i++) {
  Serial.print(muca.grid[i] + 100 ) ;
  Serial.print(",");
  }
  Serial.println("/");

}


void SendRawByte() {
  // The array is composed of 254 bytes. The two first for the minimum, the 252 others for the values.
  // HIGH byte minimum | LOW byte minimum  | value 1

  unsigned int minimum = 80000;
  uint8_t rawByteValues[254];

  for (int i = 0; i < NUM_ROWS * NUM_COLUMNS ; i++) {
  if (muca.grid[i] > 0 && minimum > muca.grid[i])  {
      minimum = muca.grid[i]; // The +30 is to be sure it's positive
    }
  }
  rawByteValues[0] = highByte(minimum);
  rawByteValues[1] = lowByte(minimum);


  for (int i = 0; i < NUM_ROWS * NUM_COLUMNS ; i++) {
    rawByteValues[i + 2] = muca.grid[i] - minimum;
    // Serial.print(rawByteValues[i+2]);
    //  Serial.print(",");

  }
  // Serial.println();
  //GetFPS();
   Serial.write(rawByteValues, 254);
   Serial.flush();
  //Serial.println();
}
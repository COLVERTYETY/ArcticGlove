#include <Arduino.h>
#include <Muca.h>

Muca muca;

bool ledstate = false;

void SendRawString();
void SendRawByte();

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
 // muca.skipLine(TX, (const short[]) { 1, 2, 3, 4 }, 4);
  //muca.skipLine(TX, (const short[]) { 14,15,16,17, 18, 19, 20, 21 }, 8);
  // muca.skipLine(RX,(const short[]) {11,12}, 2);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);  
  while(muca.init(false)==false){
    Serial.println("No touch");
    delay(1000);
  }
  Serial.println("Touch found");
  muca.useRawData(true); // If you use the raw data, the interrupt is not working

  delay(100);
  muca.setGain(31);
  // Serial.println("Gain set to 2");
}

void loop() {
  delay(300); // waiting 16ms for 60fps
  if (muca.update()) {
  //  SendRawString();
     SendRawByte(); // Faster
  }else{
    Serial.println("No touch");
  }
  digitalWrite(LED_BUILTIN, ledstate);
  ledstate = !ledstate;
}

void SendRawString() {
  // Print the array value
  for (int i = 0; i < NUM_TX * NUM_RX; i++) {
    if (muca.grid[i] >= 0) Serial.print(muca.grid[i]); // The +30 is to be sure it's positive
    if (i != NUM_TX * NUM_RX - 1)
      Serial.print(",");
  }
  Serial.println();

}


void SendRawByte() {
  // The array is composed of 254 bytes. The two first for the minimum, the 252 others for the values.
  // HIGH byte minimum | LOW byte minimum  | value 1

  unsigned int minimum = 80000;
  uint8_t rawByteValues[254];

  for (int i = 0; i < NUM_TX * NUM_RX; i++) {
  if (muca.grid[i] > 0 && minimum > muca.grid[i])  {
      minimum = muca.grid[i]; // The +30 is to be sure it's positive
    }
  }
  rawByteValues[0] = highByte(minimum);
  rawByteValues[1] = lowByte(minimum);


  for (int i = 0; i < NUM_TX * NUM_RX; i++) {
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
/*
  Synthesizer tone scanner
  
  Sets two digital pots to control an RC osciallator.  Measures the resulting pulse
  width in usecs and writes the results to the serial port.
  
  Copyright 2013 Allen B. Downey
 
  Based on an example by Tom Igoe, which is based on a tutorial by Heather Dewey-Harborg.
 
 The AD5206 is SPI-compatible,and to command it, you send two bytes, 
 one with the channel number (0 - 5) and one with the resistance value for the
 channel (0 - 255).  
 
 The circuit:
  * CS - to digital pin 10  (SS pin)
  * SDI - to digital pin 11 (MOSI pin)
  * CLK - to digital pin 13 (SCK pin)
  * Oscillator output to pin 7
 
*/


// include the SPI library:
#include <SPI.h>


// set pin 10 as the slave select for the digital pot:
const int slaveSelectPin = 10;
const int pot0 = 0;
const int pot1 = 2;
const int pulsePin = 7;
unsigned long duration;

void setup() {
  pinMode(pulsePin, INPUT);
  
  // set the slaveSelectPin as an output:
  pinMode (slaveSelectPin, OUTPUT);
  // initialize SPI:
  SPI.begin();
  
  Serial.begin(38400);
}

void loop() {
    
    for (int level1 = 1; level1 <= 255; level1++) {
        digitalPotWrite(pot0, level1);
      
        for (int level2 = 1; level2 <= 255; level2++) {
            digitalPotWrite(pot1, level2);
            delay(10);
            duration = pulseIn(pulsePin, HIGH);
            Serial.print('+');
            Serial.print(level1);
            Serial.print(' ');
            Serial.print(level2);
            Serial.print(' ');
            Serial.println(duration);
        }
    }

}

void digitalPotWrite(int address, int value) {
  // take the SS pin low to select the chip:
  digitalWrite(slaveSelectPin,LOW);
  //  send in the address and value via SPI:
  SPI.transfer(address);
  SPI.transfer(value);
  // take the SS pin high to de-select the chip:
  digitalWrite(slaveSelectPin,HIGH); 
}


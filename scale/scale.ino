
/*
  Digital Pot Control
  
  This example controls an Analog Devices AD5206 digital potentiometer.
  The AD5206 has 6 potentiometer channels. Each channel's pins are labeled
  A - connect this to voltage
  W - this is the pot's wiper, which changes when you set it
  B - connect this to ground.
 
 The AD5206 is SPI-compatible,and to command it, you send two bytes, 
 one with the channel number (0 - 5) and one with the resistance value for the
 channel (0 - 255).  
 
 The circuit:
  * All A pins  of AD5206 connected to +5V
  * All B pins of AD5206 connected to ground
  * An LED and a 220-ohm resisor in series connected from each W pin to ground
  * CS - to digital pin 10  (SS pin)
  * SDI - to digital pin 11 (MOSI pin)
  * CLK - to digital pin 13 (SCK pin)
 
 created 10 Aug 2010 
 by Tom Igoe
 
 Thanks to Heather Dewey-Hagborg for the original tutorial, 2005
 
*/


// include the SPI library:
#include <SPI.h>

#include <table.h>

// set pin 10 as the slave select for the digital pot:
const int slaveSelectPin = 10;
const int pot0 = 0;
const int pot1 = 2;
const int pulsePin = 7;

const int major_arpeggio[] = {0, 4, 7, 12};

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
    
    for (int note=30; note<40; note++) {
        play_arpeggio(note);
        delay(500);
    }

}

void play_arpeggio(int note) {
    for (int i=0; i<4; i++) {
        play_note(note + major_arpeggio[i]);
        delay(250);
    }
}

void play_note(int note) {
    digitalPotWrite(pot0, level0_table[note]);
    digitalPotWrite(pot1, level1_table[note]);  
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


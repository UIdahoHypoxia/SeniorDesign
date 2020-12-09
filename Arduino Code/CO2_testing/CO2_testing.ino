/*
  Software serial multple serial test

 Receives from the hardware serial, sends to software serial.
 Receives from software serial, sends to hardware serial.

 The circuit:
 * RX is digital pin 0 (connect to TX of other device)
 * TX is digital pin 1 (connect to RX of other device)

 Note:
 Not all pins on the Mega and Mega 2560 support change interrupts,
 so only the following can be used for RX:
 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69


 */

 /*
  * The First test software for all of the solenoids and the O2 sensor
  * 
  * Setup:
  *   Sol_1 pin 22
  *   Sol_2 pin 23
  *   Sol_3 pin 24
  *   O2 Rx - pin 10
  *   
  * Open up the serial monitor with a baud rate of 9600 and type commands to control the system
  * 
  * Commands:
  *   "open x" - opens solenoids 1-3 anything other than 1-3 will open all of them
  *   "close x" - closes solenoid x where x is 1-3 anything other than 1-3 closes all of them
  *   "read" - Begins reading the O2 sensor
  *   "stop" - stops the O2 readings from displaying
  */
#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>

#define SOL_1 22
#define SOL_2 23
#define SOL_3 24

String inputString;         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
int selection = 0;
bool displayO2 = false;
SoftwareSerial mySerial(10,14); // RX, TX

void setup()
{
   pinMode(SOL_1, OUTPUT);
   pinMode(SOL_2, OUTPUT);
   pinMode(SOL_3, OUTPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }


  Serial.println("Serial Connected");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
}

void loop() // run over and over
{
  if (mySerial.available() && displayO2)
        Serial.write(mySerial.read());
  if(stringComplete) {  
    //inputString.toLowerCase();  
    if(inputString.substring(0,4) == "read") {
      displayO2 = true;
    } 
    else if(inputString.substring(0,4) == "stop") {
      displayO2 = false;
    }
    else {
       mySerial.print(inputString);
    }
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
 
  }
}

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
  * The First test software for parsing O2 and CO2 Readings
  * 
  * Setup:
  * 
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
String O2Reading;
String CO2Reading;
float Temperature;
float O2Percent;
int CO2PPM;
bool stringComplete = false;  // whether the string is complete
int selection = 0;
bool displayO2 = false;
//SoftwareSerial O2Serial(10,18); // RX, TX
//SoftwareSerial CO2Serial(11, 16); //RX TX
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
  Serial1.begin(9600);
  Serial2.begin(9600);
}

void loop() // run over and over
{
//  if (Serial1.available() && displayO2){
//        O2Reading = Serial1.readStringUntil('\n');
//        Temperature = O2Reading.substring(12, 16).toFloat();
//        O2Percent = O2Reading.substring(26,32).toFloat();
//        Serial.println(O2Reading);
//        Serial.println(Temperature);
//        Serial.println(O2Percent);
//  }
  if (Serial.available() && displayO2){
        Serial2.write("Z\n\r");
        CO2Reading = Serial2.readStringUntil('\n');
        CO2PPM = CO2Reading.substring(2).toInt();
        Serial.println(CO2Reading);
        Serial.println(CO2PPM);
  }
  if(stringComplete) {  
    inputString.toLowerCase();  
    if(inputString.substring(0,4) == "open"){
      selection = inputString.substring(5).toInt();
      switch(selection){
        case 0:
          digitalWrite(SOL_1, 1);
          digitalWrite(SOL_2, 1);
          digitalWrite(SOL_3, 1);
          break;
        case 1:
          digitalWrite(SOL_1, 1);
          break;
        case 2:
          digitalWrite(SOL_2,1);
          break;
        case 3:
          digitalWrite(SOL_3, 1);
          break;
        default:
          Serial.print(selection);
          Serial.println("Error, invalid solenoid to open");
      }
      Serial.println(inputString);
    } 
    else if(inputString.substring(0,5) == "close") {
      selection = inputString.substring(6).toInt();
      switch(selection){
        case 0:
          digitalWrite(SOL_1, 0);
          digitalWrite(SOL_2, 0);
          digitalWrite(SOL_3, 0);
          break;
        case 1:
          digitalWrite(SOL_1, 0);
          break;
        case 2:
          digitalWrite(SOL_2,0);
          break;
        case 3:
          digitalWrite(SOL_3, 0);
          break;
        default:
          Serial.println("Error, invalid solenoid to Close");
      }
       Serial.println(inputString);
    } 
    else if(inputString.substring(0,4) == "read") {
      displayO2 = true;
    } 
    else if(inputString.substring(0,4) == "stop") {
      displayO2 = false;
    }
    else {
       Serial.println(inputString);
       Serial.println("Invalid Command");
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

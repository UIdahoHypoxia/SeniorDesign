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
//#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>

#define SOL_O2 22
#define SOL_CO2 23
#define SOL_Ex 24

#define upperO2 25
#define lowerCO2 0
#define upperTime 100
#define lowerTime 10

String inputString;         // a String to hold incoming data
String O2Reading;
String CO2Reading;
float Temperature;
float O2Percent;
float CO2Percent;
float Temp;
float Humidity;
float Pressure;
int CO2PPM;
bool displayO2 = false;

bool ReadSerial = false;
float CO2Setpoint = 5.0;
float O2Setpoint = 5.0;

//SoftwareSerial O2Serial(10,18); // RX, TX
//SoftwareSerial CO2Serial(11, 16); //RX TX
HardwareSerial *O2Serial = &Serial1;
HardwareSerial *CO2Serial = &Serial2;


void setup()
{
   
   pinMode(SOL_O2, OUTPUT);
   pinMode(SOL_CO2, OUTPUT);
   pinMode(SOL_Ex, OUTPUT);
   pinMode(LED_BUILTIN, OUTPUT);
   
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }
  Serial.println("Serial Connected");

  // set the data rate for the two Serial ports: Serial1=O2, Serial2=CO2
  O2Serial->begin(9600);
  CO2Serial->begin(9600);
  setupTimer(15624);
}

void loop() // run over and over
{
  if(ReadSerial){
    readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
    if(O2Percent <= 25 && CO2Percent <= 10) {
      ControlSolenoids(O2Percent, CO2Percent, O2Setpoint, CO2Setpoint);
    }
    ReadSerial = false;
    
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
      CommandParse(inputString);
      inputString = "";
    }
  }
}

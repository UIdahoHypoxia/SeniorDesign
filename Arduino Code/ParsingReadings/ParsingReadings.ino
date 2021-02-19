/*
  *
  * The First test software for parsing O2 and CO2 Readings
  * 
  * Setup:
  * 
  *   O2 Rx - pin 19 - RX1
  *   O2 Tx - pin 18 - TX1
  *   
  *   CO2 RX - pin 17 - RX2
  *   CO2 Tx - Pin 16 - TX2
  *   
  * Open up the serial monitor with a baud rate of 9600 and type commands to control the system
  * 
  * Commands:
  *   "open x" - opens solenoids 1-3 anything other than 1-3 will open all of them
  *   "close x" - closes solenoid x where x is 1-3 anything other than 1-3 closes all of them
  */
#include <stdio.h>
#include <string.h>

#define SOL_O2 22
#define SOL_CO2 23
#define SOL_Ex 24

#define upperO2 25      // upper limit of the O2 sensor
#define lowerCO2 0      // Lower limit of the CO2 sensor
#define upperTime 100   // Max time the solenoid can open for at once
#define lowerTime 10    // Min time for solenoid opening

#define readTime 3     // Time between sensor readings and solenoids, in seconds

float CO2Setpoint = 5.0;
float O2Setpoint = 5.0;


String inputString;         // a String to hold incoming data
float Temperature;
float O2Percent;
float CO2Percent;
float Temp;
float Humidity;
float Pressure;
int CO2PPM;

//bool ReadSerial = false; // Outdated, used with the timer

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
  //setupTimer(15624);
}

void loop() // run over and over
{
  /*static int timerDelay = 0;
  if(ReadSerial){
    if(timerDelay == readTime){
      readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
      if(O2Percent <= 25 && CO2Percent <= 10) {
        ControlSolenoids(O2Percent, CO2Percent, O2Setpoint, CO2Setpoint);
      }
      timerDelay = 0;
    } else if(timerDelay == readTime-1){
        if (O2Serial->available()) {
            O2ReadingTest = O2Serial->readStringUntil('\n');
        }
    }
    ReadSerial = false;
    timerDelay++;    
  }  */

  
  static unsigned long previous = millis();
  // Used to track if when readings() is called it receives a good O2 reading.
  // 1: Good last reading
  // 0: Bad last reading
  //The goal is to always have read a poor reading in the off cycle and not calculate based on it so that the good reading comes through at the Delay time
  int goodReading = 0; 
  
  if(CheckTime(&previous, readTime*1000)){ //readTime is a #define above that is multiplied by 1000 to get the millisecond equivalent
      goodReading = readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
      ControlSolenoids(O2Percent, CO2Percent, O2Setpoint, CO2Setpoint);
  } 
  if(goodReading == 1){ // implemented to avoid the issue of every other O2 reading being extra long and bad. This only happened when increasing the delay time over 1s for some reason
      Serial.println("Offset:");
      goodReading = readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
  }
}


//Used to capture the serial command inputs sent by the user over the serial 1 line.
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

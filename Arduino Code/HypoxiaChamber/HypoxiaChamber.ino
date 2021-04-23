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
#include <PID_v1.h>

//#define Debug 1

#define SOL_O2 25
#define SOL_CO2 24
#define SOL_Ex 22

#define O2_Power 52

#define UpperO2Time 2000   // Max time the solenoid can open for at once
#define UpperCO2Time 1200

#define readTime 7 // Time between sensor readings and solenoids, in seconds

double CO2Setpoint = 5.0;
double O2Setpoint = 1.0;

double O2Kp=140, O2Ki=5, O2Kd=0;

double CO2Kp=150, CO2Ki=5, CO2Kd=0;

int Debug = 0;
String inputString;         // a String to hold incoming data
float Temperature;
double O2Percent;
double CO2Percent;
double O2Solenoid;
double CO2Solenoid;
float Temp;
float Humidity;
float Pressure;
int CO2PPM;

//bool ReadSerial = false; // Outdated, used with the timer

HardwareSerial *O2Serial = &Serial1;
HardwareSerial *CO2Serial = &Serial2;

int pause = 0;
int GO = 0;
int O2Errors = 0;
int O2_OnOff = 1;
void setup()
{
   pinMode(SOL_O2, OUTPUT);
   pinMode(SOL_CO2, OUTPUT);
   pinMode(SOL_Ex, OUTPUT);
   pinMode(O2_Power, OUTPUT);
   pinMode(LED_BUILTIN, OUTPUT);
   digitalWrite(O2_Power, 1);
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }
  //Serial.println("Serial Connected");
  //Serial.println("O2, CO2, Temp, Humid, Pressure, O2Solenoid, CO2Solenoid");

  // set the data rate for the two Serial ports: Serial1=O2, Serial2=CO2
  O2Serial->begin(9600);
  CO2Serial->begin(9600);
}

void loop() // run over and over
{  
  static unsigned long previous = millis();
  // 1: Good last reading
  // 0: Bad last reading
  //The goal is to always have read a poor reading in the off cycle and not calculate based on it so that the good reading comes through at the Delay time
  int goodReading = 0; 
 
  if(GO){
    if(CheckTime(&previous, readTime*1000)){ //readTime is a #define above that is multiplied by 1000 to get the millisecond equivalent
        goodReading = readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
        O2Solenoid = -1; // Default to -1 so that whenever a solenoid does not get controlled it sends a -1 and the user can tell when the solenoids are opening or not.
        CO2Solenoid = -1;
        if((O2Percent < 25 && (CO2Percent >= (CO2Setpoint  * 0.9)) && (O2Percent > (O2Setpoint*1.01))) && !pause){
          O2Solenoid = ControlO2(O2Percent, O2Setpoint, O2Kp, O2Ki, O2Kd);
          O2Errors = 0;
        } else if (O2Percent == 100){
          O2Errors++;
          Serial.print("O2Errors:");
          Serial.println(O2Errors);

          Serial.print("O2Power:");
          Serial.println(O2_OnOff);
          if(O2Errors >= 3 && O2_OnOff == 1){
            digitalWrite(O2_Power, 0);
            O2_OnOff = 0;
            O2Errors = 0;
          } else if (O2Errors >= 3 && O2_OnOff == 0){
            digitalWrite(O2_Power, 1);
            O2_OnOff = 1;
            O2Errors = 0;
          }
        }
        delay(50);
        if((CO2Percent < 10 && (CO2Percent < (CO2Setpoint*0.98))) && !pause) {
          CO2Solenoid = ControlCO2(CO2Percent, CO2Setpoint, CO2Kp, CO2Ki, CO2Kd);
        }
        Serial.print("V:");
        Serial.print(O2Percent);
        Serial.print(",");
        Serial.print(CO2Percent);
        Serial.print(",");
        Serial.print(Temp);
        Serial.print(",");
        Serial.print(Humidity);
        Serial.print(",");
        Serial.print(Pressure);
        Serial.print(",");
        Serial.print(O2Solenoid);
        Serial.print(",");
        Serial.print(CO2Solenoid);
        Serial.print("\n");
        digitalWrite(LED_BUILTIN, LOW);
    } 
    if(goodReading == 1){ // implemented to avoid the issue of every other O2 reading being extra long and bad. This only happened when increasing the delay time over 1s for some reason
        //Serial.println("Offset:");
        goodReading = readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure);
    }
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

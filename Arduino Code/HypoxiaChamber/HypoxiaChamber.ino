/*
  *
  * The arduino code to run on an Arduino Mega board.
  * 
  * Used to control a Hypoxia Chamber in tandem with the python GUI code
  * 
  * Setup:
  * 
  *   O2 Rx - Pin 19 - RX1
  *   O2 Tx - Pin 18 - TX1
  *   
  *   CO2 RX - Pin 17 - RX2
  *   CO2 Tx - Pin 16 - TX2
  *   
  *   O2 Power - Pin 52
  *   
  * The device communicates over a serial connection at baud rate 115200 to python code running on a connected device via the USB cable.  
  * To control directly from the serial monitor, open up the serial monitor with a baud rate of 115200 and type commands to control the system via the arduino serial monitor
  * 
  * Commands:
  *   "open x" - opens solenoids 1-3 anything other than 1-3 will open all of them
  *   "close x" - closes solenoid x where x is 1-3 anything other than 1-3 closes all of them
  *   "O2 x.x" - Sets the O2 setpoint to the float specified in x.x
  *   "CO2 x.x" -  Sets the CO2 setpoint to the float specified in x.x
  *   "Debug" - Turns on Debug print statements in the O2 and CO2 control functions
  *   "Pause" - Pauses the opening of solenoids but continues to read and transmit sensor data
  *   "Start" - Starts the whole experiment
  *   "Stop" - Stops the experiment, control of the solenoids, data collection, and data transmission
  *   "time x" - Sets the time intervals for reading sensors and controlling the solenoids. (Default 10 seconds)
  *   "KpO2 x.x" - Set the Kp value for the O2 PID object created, needs to be set before starting the experiment
  *   "KiO2 x.x" - Set the Ki value for the O2 PID object created, needs to be set before starting the experiment
  *   "KpCO2 x.x" - Set the Kp value for the CO2 PID object created, needs to be set before starting the experiment
  *   "KiCO2 x.x" - Set the Ki value for the CO2 PID object created, needs to be set before starting the experiment
  */
#include <stdio.h>
#include <string.h>
#include <PID_v1.h>

#define SOL_O2 25               //O2 solenoid control pin
#define SOL_CO2 24              //CO2 solenoid control pin
#define SOL_Ex 22               //Exhaust solenoid control pin

#define O2_Power 52             //O2 Sensor power control pin

#define UpperO2Time 2000        // Max time the solenoid can open for at once for the O2 solenoid
#define UpperCO2Time 1200       // Max time the solenoid can open for at once for the CO2 solenoid



int readTime = 10;              // Time between sensor readings and solenoids, in seconds
double CO2Setpoint = 5.0;       // CO2 Setpoint to reach
double O2Setpoint = 1.0;        // O2 Setpoint to reach

double O2Kp=140, O2Ki=5, O2Kd=0; //Defualt PID constants for O2

double CO2Kp=150, CO2Ki=5, CO2Kd=0; //Defualt PID constants for the CO2

int Debug = 0;                  // Variable storing whether or not Debug mode is enabled, print commands in the control functions, 0=Off, 1=On
String inputString;             // a String to hold incoming data form serial communication
double O2Percent;               //O2 Percentage value read from Sensor
double CO2Percent;              //CO2 Percentage value read from Sensor
double O2Solenoid;              //Time calculated to open the O2 solenoid
double CO2Solenoid;             //Time calculated to open the CO2 solenoid
float Temp;                     //Temperature value read from Sensor
float Humidity;                 //Humidity value read from Sensor
float Pressure;                 //Pressure value read from Sensor
int pause = 0;                  //Controls if the system is paused, 0=running, 1=paused
int GO = 0;                     //Controls if the system is actively running, 0=Stopped, 1=running
int O2Errors = 0;               //Tracks O2 sensor bad readings
int O2_OnOff = 1;               //Controls output of O2 sensor power on pin 52

HardwareSerial *O2Serial = &Serial1;  //Creates Serial connection for the O2 Sensor connected to Tx1 and Rx1
HardwareSerial *CO2Serial = &Serial2; //Creates Serial connection for the CO2 Sensor connected to Tx2 and Rx2


void setup()
{
   //Setup pins for the solenoid as outputs
   pinMode(SOL_O2, OUTPUT);
   pinMode(SOL_CO2, OUTPUT);
   pinMode(SOL_Ex, OUTPUT);
   pinMode(O2_Power, OUTPUT);
   pinMode(LED_BUILTIN, OUTPUT);
   digitalWrite(O2_Power, 1);     //Defalt the O2 sensor on
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
 
  if(GO){           //If the start command has been given
    if(CheckTime(&previous, readTime*1000)){ //readTime is a defined variable above that is multiplied by 1000 to get the millisecond equivalent
        goodReading = readings(&O2Percent, &CO2Percent, &Temp, &Humidity, &Pressure); //Takes the readings from the two sensors and stores it into the appropriate variables, saves if the O2 reading worked into the return variable
        O2Solenoid = -1; // Default to -1 so that whenever a solenoid does not get controlled it sends a -1 and the user can tell when the solenoids are opening or not.
        CO2Solenoid = -1;
        if((O2Percent < 25 && (CO2Percent >= (CO2Setpoint  * 0.9)) && (O2Percent > (O2Setpoint*1.01))) && !pause){    //Checks if the O2 reading is within bounds and that the CO2 setpoint has been almost reached. Also checks if the O2setpoint is overreached to stop so that it does not overshoot
          O2Solenoid = ControlO2(O2Percent, O2Setpoint, O2Kp, O2Ki, O2Kd);                                            //Controls the O2 solenoids and returns the amount of time the solenoid is opened.
          O2Errors = 0;
        } else if (O2Percent == 100){                                                                                 //If a bad O2 reading came in then ignore it and increase the error count. When reading from the O2 sensor, it occasionally gets bad serial communications and restarts mid way through a line,this ignores those
          O2Errors++;
          Serial.print("O2Errors:");
          Serial.println(O2Errors);

          Serial.print("O2Power:");                                                                           
          Serial.println(O2_OnOff);
          if(O2Errors >= 3 && O2_OnOff == 1){                                                                        //If the O2 sensor has been giving bad readings 3 times in a row, then turn off the sensor for 3 cycles and turn it back on. This is a poor fix for the issue, but we could not figure out why the O2 sensor was giving bad readings within our timeframe     
            digitalWrite(O2_Power, 0);
            O2_OnOff = 0;
            O2Errors = 0;
          } else if (O2Errors >= 3 && O2_OnOff == 0){                                                                 //Turns the O2 sensor back on
            digitalWrite(O2_Power, 1);
            O2_OnOff = 1;
            O2Errors = 0;
          }
        }
        delay(50);                                                                                                    // Wait 50ms after controlling the O2 solenoids to control the CO2 ones
        if((CO2Percent < 20 && (CO2Percent < (CO2Setpoint*0.98))) && !pause) {                                        // If the current CO2 reading is within reason, below the max of the sensor and not too close to the setpoint
          CO2Solenoid = ControlCO2(CO2Percent, CO2Setpoint, CO2Kp, CO2Ki, CO2Kd);                                     //Control the CO2 solenoid based on the setpoints and PID constants, return the time open for the solenoid
        }
        Serial.print("V:");                                                                                           //Prints all of the information to the serial interface, this is what communicates it to the Python GUI
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
        //digitalWrite(LED_BUILTIN, LOW);
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

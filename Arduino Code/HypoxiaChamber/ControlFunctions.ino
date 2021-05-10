
//The main function to parse the commands coming in over the USB Serial interface. All of the commands and functions are outlined at the top of HypoxiaChamber.ino
void CommandParse(String input){
  int selection = 0;
  if(input.substring(0,4) == "open"){
      selection = input.substring(5).toInt();
      switch(selection){
        case 0:
          digitalWrite(SOL_O2, 1);
          digitalWrite(SOL_CO2, 1);
          digitalWrite(SOL_Ex, 1);
          break;
        case 1:
          digitalWrite(SOL_O2, 1);
          break;
        case 2:
          digitalWrite(SOL_CO2,1);
          break;
        case 3:
          digitalWrite(SOL_Ex, 1);
          break;
        default:
          Serial.print(selection);
          Serial.println("Error, invalid solenoid to open");
      }
      Serial.println(input);
    } 
    else if(input.substring(0,5) == "close") {
      selection = input.substring(6).toInt();
      switch(selection){
        case 0:
          digitalWrite(SOL_O2, 0);
          digitalWrite(SOL_CO2, 0);
          digitalWrite(SOL_Ex, 0);
          break;
        case 1:
          digitalWrite(SOL_O2, 0);
          break;
        case 2:
          digitalWrite(SOL_CO2,0);
          break;
        case 3:
          digitalWrite(SOL_Ex, 0);
          break;
        default:
          Serial.println("Error, invalid solenoid to Close");
      }
       Serial.println(input);
    } 
    else if(input.substring(0,2) == "O2") {
      O2Setpoint = input.substring(3).toFloat();
    }
    else if(input.substring(0,3) == "CO2") {
      CO2Setpoint = input.substring(4).toFloat();
      Serial.println(CO2Setpoint);
    }
    else if(input.substring(0,5) == "Debug"){
      Debug = (Debug+1)%2;
    }
    else if(input.substring(0,5) == "Pause") {
      pause = !pause;
    } 
    else if(input.substring(0,5) == "Start") {
      GO = 1;
    }
    else if(input.substring(0,4) == "Stop") {
      GO = 0;
    }
    else if(input.substring(0,4) == "time"){
      readTime = input.substring(4).toInt();
    }
    else if(input.substring(0,4) == "KpO2"){
      O2Kp = input.substring(4).toFloat();
    }
    else if(input.substring(0,4) == "KiO2"){
      O2Ki = input.substring(4).toFloat();
    }
    else if(input.substring(0,5) == "KpCO2"){
      CO2Kp = input.substring(5).toFloat();
    }
    else if(input.substring(0,5) == "KiCO2"){
      CO2Ki = input.substring(5).toFloat();
    }
    else {
       digitalWrite(LED_BUILTIN, HIGH);
       Serial.println(input);
       Serial.println("Invalid Command");
    }
}


//Controls the O2 solenoid based on the input O2 percent reading, O2 setpoint, and PID constants. The PID constants are only used on the first call of this function to create a static PID object from the <PID_v1.h> library. Returns the amount of time in milliseconds that the O2 solenoid was opened.
double ControlO2(double O2Percent, double O2Set, double Kp, double Ki, double Kd){
  static double Output;
  static double adjustedSetpoint, adjustedO2;
  adjustedSetpoint = 30 - O2Set;    //Because the PID library can only work up to a setpoint and not down, the O2 values are subtracted from 30 to invert them
  adjustedO2 = 30-O2Percent;
  static PID myPID(&adjustedO2, &Output, &adjustedSetpoint, Kp, Ki, Kd, DIRECT);    //Creates the PID setpoint, the 
  static int Setup = 0;
  /*Serial.print("ControlO2 Params:");
  Serial.print(O2Percent);
  Serial.print(", ");
  Serial.print(O2Set);
  Serial.print(", ");
  Serial.print(Kp);
  Serial.print(", ");
  Serial.print(Ki);
  Serial.print(", ");
  Serial.println(Kd);*/
  if(!Setup) {                              //Only ran the first run through of the function
    Serial.println("O2 PID Setup");
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(0, UpperO2Time);  //Limits the O2 solenoid output to the defined upper limit, even if the PID calculates a higher value
    Setup = 1;
  }
  myPID.Compute();                          //Computes the PID loop based on the pointer inputs and stores the result in Output
  /*Serial.print("O2 PID Output:");
  Serial.println(Output);*/
  //digitalWrite(LED_BUILTIN, 1);         //Opens the exhaust solenoid first then the O2 solenoid, delays for the specified time and then closes O2 then exhaust
  digitalWrite(SOL_Ex, 1);
  digitalWrite(SOL_O2, 1);
  delay(Output);
  //digitalWrite(LED_BUILTIN, 0);
  digitalWrite(SOL_O2, 0);
  digitalWrite(SOL_Ex, 0);
  return Output;
}
//Controls the CO2 solenoid based on the input CO2 percent reading, CO2 setpoint, and PID constants. The PID constants are only used on the first call of this function to create a static PID object from the <PID_v1.h> library. Returns the amount of time in milliseconds that the CO2 solenoid was opened.
//Behaves in the same way as the ControlO2() function, however, it does not have to invert the CO2 values because they are working up towards a setpoint
double ControlCO2(double CO2Percent, double CO2Set, double Kp, double Ki, double Kd){
  static double Output;
  static PID myPID(&CO2Percent, &Output, &CO2Set, Kp, Ki, Kd, DIRECT);
  static int Setup = 0;
  if(!Setup) {
    Serial.println("CO2 PID Setup");
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(0, UpperCO2Time);
    Setup = 1;
  }
  myPID.Compute();
  //digitalWrite(LED_BUILTIN, 1);
  digitalWrite(SOL_Ex, 1);
  digitalWrite(SOL_CO2, 1);
  delay(Output);
  //digitalWrite(LED_BUILTIN, 0);
  digitalWrite(SOL_CO2, 0);
  digitalWrite(SOL_Ex, 0);
  return Output;
}

/*Gets the readings of the O2 and CO2 sensors and stores them in the passed by reference variables. 
 * The O2 sensor is constantly sending serial communications of its data, reference the manual for info of organization (https://cdn.shopify.com/s/files/1/0406/7681/files/Manual-Luminox-LOX-02-CO2-Sensor.pdf)
 *      The O2 percent and temperature are read from the O2 sensor
 * The CO2 sensor needs to be polled to get data from it. It is sent commands based on the predefined commands in the manual (http://co2meters.com/Documentation/Manuals/Manual_GC_0024_0025_0026_Revised8.pdf)
 * 
  */
int readings( double *O2Percent, double *CO2Percent, float *Temp, float *Humidity, float *Pressure) {
  String CO2Reading, O2Reading, HReading, PReading;
  CO2Serial->println("Z");        //Request CO2 from sensor
  int retval = 1;
  if (O2Serial->available()) {          //If the O2 communicated over serial, read the string and parse it into its necessary sections. Pulling out temp and O2 percent
    O2Reading = O2Serial->readStringUntil('\n');
    if(O2Reading.length() < 42 && O2Reading.length() > 35){
      *O2Percent = O2Reading.substring(26,32).toDouble();
      *Temp = O2Reading.substring(12,16).toFloat();
      if(Debug) Serial.println("O2:"+O2Reading);
      if(Debug) Serial.println("O2%:"+ (String)*O2Percent);
      if(Debug) Serial.println("O2 T:"+ (String)*Temp);
    } else {
      if(Debug) Serial.println("Bad O2:" + O2Reading);
      *O2Percent = 100;
      retval = 0;
    }
  }
  delay(50);
  if (CO2Serial->available()) {       //If the CO2 is communicating over serial parse what it sent in response to the "Z" command.
    CO2Reading = CO2Serial->readStringUntil('\n');
    if((CO2Reading.length() < 9) && (CO2Reading.substring(0,1) != "E")) {
      *CO2Percent = CO2Reading.substring(2,7).toFloat()/1000;
      if(Debug) Serial.println("CO2:"+CO2Reading);
      if(Debug) Serial.println("CO2 %:" + (String)*CO2Percent);
    } else {
      if(Debug) Serial.println("CO2 Bad="+CO2Reading);
      *CO2Percent = 100;
    }
  }

  delay(50);
  CO2Serial->println("H");        //Send a humidity request and parse the response into the appropriate variable
  delay(50);
  if (CO2Serial->available()) {
    HReading = CO2Serial->readStringUntil('\n');
    if((HReading.length() < 9) && (HReading.substring(0,1) != "E")) {
      *Humidity = HReading.substring(2,7).toFloat()/10;
      if(Debug) Serial.println("H:" + HReading);
      if(Debug) Serial.println("H %:" + (String)*Humidity);
    } else {
      if(Debug) Serial.println("H Bad:" +HReading);
    }
  }
  delay(50);
  CO2Serial->println("B");        //Send a pressure request and parse the response into the appropriate variable
  delay(50);
  if (CO2Serial->available()) {
    PReading = CO2Serial->readStringUntil('\n');
    if((PReading.length() < 9) && (PReading.substring(0,1) != "E")) {
      *Pressure = PReading.substring(2,7).toFloat()/10;
      if(Debug) Serial.println("P: " + PReading);
      if(Debug) Serial.println("P #: " + (String)*Pressure);
    } else {
      if(Debug) Serial.println("P Bad: " +PReading);
    }
  }
  return retval;                    //Returns if there was a bad O2 reading

}

int CheckTime(unsigned long *previous, unsigned long delay){
  unsigned long currentTime = millis();
  int retval = 0;
  if(currentTime - *previous >= delay){
    retval = 1;
    *previous = currentTime;
  }
  return retval;
}

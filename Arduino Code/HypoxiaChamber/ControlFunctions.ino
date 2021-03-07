

void CommandParse(String input){
  int selection = 0;
  String CO2Reading;
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
      CO2Serial->print(input.substring(4));
      if (CO2Serial->available()) {
        CO2Reading = CO2Serial->readStringUntil('\n');
        Serial.println("CO2 Command Return" + CO2Reading);
      }
    }
    else if(input.substring(0,5) == "Debug"){
      Debug = (Debug+1)%2;
    }
    else {
       Serial.println(input);
       Serial.println("Invalid Command");
    }
}

double ControlO2(double O2Percent, double O2Set, double Kp, double Ki, double Kd){
  static double Output;
  static double adjustedSetpoint, adjustedO2;
  adjustedSetpoint = 30 - O2Set;
  adjustedO2 = 30-O2Percent;
  static PID myPID(&adjustedO2, &Output, &adjustedSetpoint, Kp, Ki, Kd, DIRECT);
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
  if(!Setup) {
    Serial.println("O2 PID Setup");
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(0, UpperO2Time);
    Setup = 1;
  }
  myPID.Compute();
  /*Serial.print("O2 PID Output:");
  Serial.println(Output);*/
  digitalWrite(LED_BUILTIN, 1);
  digitalWrite(SOL_Ex, 1);
  digitalWrite(SOL_O2, 1);
  delay(Output);
  digitalWrite(LED_BUILTIN, 0);
  digitalWrite(SOL_O2, 0);
  digitalWrite(SOL_Ex, 0);
  return Output;
}

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
  digitalWrite(LED_BUILTIN, 1);
  digitalWrite(SOL_Ex, 1);
  digitalWrite(SOL_CO2, 1);
  delay(Output);
  digitalWrite(LED_BUILTIN, 0);
  digitalWrite(SOL_CO2, 0);
  digitalWrite(SOL_Ex, 0);
  return Output;
}

int readings( double *O2Percent, double *CO2Percent, float *Temp, float *Humidity, float *Pressure) {
  String CO2Reading, O2Reading, HReading, PReading;
  CO2Serial->println("Z");
  int retval = 1;
  if (O2Serial->available()) {    
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
  if (CO2Serial->available()) {
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
  CO2Serial->println("H");
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
  CO2Serial->println("B");
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
  return retval;

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

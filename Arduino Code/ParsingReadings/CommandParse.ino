

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
    else {
       Serial.println(input);
       Serial.println("Invalid Command");
    }
}

void ControlSolenoids(float O2Percent, float CO2Percent, float O2Set, float CO2Set, float *timeOpenO2, float *timeOpenCO2){
  if(CO2Percent <= 10){
    if((CO2Set - CO2Percent) > 0.1){
      float a = (CO2Set - CO2Percent);
      float b = (CO2Percent - lowerCO2);
      *timeOpenCO2 = ((upperTime * a + lowerTime*b)/(a+b));
      if(Debug) Serial.println(*timeOpenCO2);
      digitalWrite(LED_BUILTIN, 1);
      digitalWrite(SOL_Ex, 1);
      digitalWrite(SOL_CO2, 1);
      delay(*timeOpenCO2);
      digitalWrite(LED_BUILTIN, 0);
      digitalWrite(SOL_CO2, 0);
      digitalWrite(SOL_Ex, 0);
    }
  }
  if (O2Percent <= 25) {
    if ((CO2Set - CO2Percent) < 0.5) {
      if((O2Percent - O2Set) > 0.1){
        float a = (upperO2-O2Percent);
        float b = (O2Percent - O2Set);
        *timeOpenO2 = ((upperTime * b + lowerTime*a)/(a+b));
        if(Debug) Serial.println(*timeOpenO2);
        digitalWrite(LED_BUILTIN, 1);
        digitalWrite(SOL_Ex, 1);
        digitalWrite(SOL_O2, 1);
        delay(*timeOpenO2);
        digitalWrite(LED_BUILTIN, 0);
        digitalWrite(SOL_O2, 0);
        digitalWrite(SOL_Ex, 0);
      }
    }
  }
}

int readings( float *O2Percent, float *CO2Percent, float *Temp, float *Humidity, float *Pressure) {
  String CO2Reading, O2Reading, HReading, PReading;
  CO2Serial->println("Z");
  int retval = 1;
  if (O2Serial->available()) {    
    O2Reading = O2Serial->readStringUntil('\n');
    if(O2Reading.length() < 42){
      *O2Percent = O2Reading.substring(26,32).toFloat();
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

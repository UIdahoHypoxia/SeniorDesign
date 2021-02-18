

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
    else if(input.substring(0,4) == "read") {
      displayO2 = true;
    } 
    else if(input.substring(0,4) == "stop") {
      displayO2 = false;
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

void ControlSolenoids(float O2Percent, float CO2Percent, float O2Set, float CO2Set){
  float timeOpenO2, timeOpenCO2;
  if((CO2Set - CO2Percent) > 0.1){
    float a = (CO2Set - CO2Percent);
    float b = (CO2Percent - lowerCO2);
    timeOpenCO2 = ((upperTime * a + lowerTime*b)/(a+b));
    Serial.println(timeOpenCO2);
    digitalWrite(LED_BUILTIN, 1);
    digitalWrite(SOL_Ex, 1);
    digitalWrite(SOL_CO2, 1);
    delay(timeOpenCO2);
    digitalWrite(LED_BUILTIN, 0);
    digitalWrite(SOL_CO2, 0);
    digitalWrite(SOL_Ex, 0);
  }

  if ((CO2Set - CO2Percent) < 0.5) {
    if((O2Percent - O2Set) > 0.1){
      float a = (upperO2-O2Percent);
      float b = (O2Percent - O2Set);
      timeOpenO2 = ((upperTime * b + lowerTime*a)/(a+b));
      Serial.println(timeOpenO2);
      digitalWrite(LED_BUILTIN, 1);
      digitalWrite(SOL_Ex, 1);
      digitalWrite(SOL_O2, 1);
      delay(timeOpenO2);
      digitalWrite(LED_BUILTIN, 0);
      digitalWrite(SOL_O2, 0);
      digitalWrite(SOL_Ex, 0);
    }
  }
}

int readings( float *O2Percent, float *CO2Percent, float *Temp, float *Humidity, float *Pressure) {
  String CO2Reading, O2Reading, HReading, PReading;
  String scrap;
  CO2Serial->println("Z");
  int retval = 1;
  if (O2Serial->available()) {    
    O2Reading = O2Serial->readStringUntil('\n');
    if(O2Reading.length() < 42){
      *O2Percent = O2Reading.substring(26,32).toFloat();
      *Temp = O2Reading.substring(12,16).toFloat();
      Serial.println("O2:"+O2Reading);
      Serial.println("O2%:"+ (String)*O2Percent);
      Serial.println("O2 T:"+ (String)*Temp);
    } else {
      Serial.println("Bad O2:" + O2Reading);
      *O2Percent = 100;
      retval = 0;
    }
  }
  delay(50);
  if (CO2Serial->available()) {
    CO2Reading = CO2Serial->readStringUntil('\n');
//    if (CO2Reading.substring(0,1) != "Z") {
//       CO2Reading = CO2Serial->readStringUntil('\n');
//       Serial.println("yes");
//    }
    if((CO2Reading.length() < 9) && (CO2Reading.substring(0,1) != "E")) {
      *CO2Percent = CO2Reading.substring(2,7).toFloat()/1000;
      Serial.println("CO2:"+CO2Reading);
      Serial.println("CO2 %:" + (String)*CO2Percent);
    } else {
      Serial.println("CO2 Bad="+CO2Reading);
      *CO2Percent = 100;
    }
  }

  delay(50);
  CO2Serial->println("H");
  delay(50);
  if (CO2Serial->available()) {
    HReading = CO2Serial->readStringUntil('\n');
//    if (HReading.substring(0,1) != "H") {
//       HReading = CO2Serial->readStringUntil('\n');
//    }
    if((HReading.length() < 9) && (HReading.substring(0,1) != "E")) {
      *Humidity = HReading.substring(2,7).toFloat()/10;
      Serial.println("H:" + HReading);
      Serial.println("H %:" + (String)*Humidity);
    } else {
      Serial.println("H Bad:" +HReading);
    }
  }
  delay(50);
  CO2Serial->println("B");
  delay(50);
  if (CO2Serial->available()) {
    PReading = CO2Serial->readStringUntil('\n');
//    if (PReading.substring(0,1) != "B") {
//       PReading = CO2Serial->readStringUntil('\n');
//    }
    if((PReading.length() < 9) && (PReading.substring(0,1) != "E")) {
      *Pressure = PReading.substring(2,7).toFloat()/10;
      Serial.println("P: " + PReading);
      Serial.println("P #: " + (String)*Pressure);
    } else {
      Serial.println("P Bad: " +PReading);
    }
//    scrap = CO2Serial -> readStringUntil('\n');
//    Serial.println("scrap3="+scrap);
  }
  return retval;

}

void setupTimer(int CompareMatch){
  cli();
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = CompareMatch;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei();
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

ISR(TIMER1_COMPA_vect){//timer1 interrupt 1Hz toggles pin 13 (LED)
//generates pulse wave of frequency 1Hz/2 = 0.5kHz (takes two cycles for full wave- toggle high then toggle low)
  //ReadSerial = true;
  if (ReadSerial){
    digitalWrite(LED_BUILTIN,HIGH);
    ReadSerial = 0;
  }
  else{
    digitalWrite(LED_BUILTIN,LOW);
    ReadSerial = 1;
  }
}



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
    else if(input.substring(0,4) == "read") {
      displayO2 = true;
    } 
    else if(input.substring(0,4) == "stop") {
      displayO2 = false;
    }
    else {
       Serial.println(input);
       Serial.println("Invalid Command");
    }
}

void ControlSolenoids(float O2Percent, float CO2Percent, float O2Set, float CO2Set){
  float timeOpenO2, timeOpenCO2;
  if((O2Percent - O2Set) > 0.1){
    timeOpenO2 = ((upperTime * (O2Percent-O2Set)) + lowerTime*(upperO2-O2Set))/((O2Percent-O2Set)+(upperO2-O2Set));
    Serial.println(timeOpenO2);
    digitalWrite(LED_BUILTIN, 1);
    digitalWrite(SOL_Ex, 1);
    digitalWrite(SOL_O2, 1);
    delay(timeOpenO2);
    digitalWrite(LED_BUILTIN, 0);
    digitalWrite(SOL_O2, 0);
    digitalWrite(SOL_Ex, 0);
  }

  if((CO2Percent - O2Set) > 0.1){
    timeOpenCO2 = ((upperTime * (CO2Percent-CO2Set)) + lowerTime*(upperO2-CO2Set))/((CO2Percent-CO2Set)+(upperO2-CO2Set));
    Serial.println(timeOpenCO2);
    digitalWrite(LED_BUILTIN, 1);
    digitalWrite(SOL_Ex, 1);
    digitalWrite(SOL_CO2, 1);
    delay(timeOpenCO2);
    digitalWrite(LED_BUILTIN, 0);
    digitalWrite(SOL_CO2, 0);
    digitalWrite(SOL_Ex, 0);
  }
  
}

int readings(float O2Setpoint, float CO2Setpoint, float *O2Percent, float *CO2Percent) {
  String CO2Reading, O2Reading;
  CO2Serial->write("Z\n\r");
  if (CO2Serial->available()) {
    CO2Reading = CO2Serial->readStringUntil('\n');
    *CO2Percent = CO2Reading.substring(2).toFloat()/1000;
    Serial.println(CO2Reading);
  }
  if (O2Serial->available()) {
    O2Reading = O2Serial->readStringUntil('\n');
    *O2Percent = O2Reading.substring(26,32).toFloat();
    Serial.println(O2Reading);
    Serial.println(*O2Percent);
  }

  return 1;
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

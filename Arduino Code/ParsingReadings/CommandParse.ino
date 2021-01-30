

void CommandParse(String input){
  int selection = 0;
  if(input.substring(0,4) == "open"){
      selection = input.substring(5).toInt();
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
      Serial.println(input);
    } 
    else if(input.substring(0,5) == "close") {
      selection = input.substring(6).toInt();
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
       Serial.println(input);
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

void ControlSolenoids(


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

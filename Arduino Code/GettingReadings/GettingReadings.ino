void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  if (flag_set == true) {
    sols = readings();
  }
}

int readings(O2Setpoint, CO2Setpoint) {
  CO2Serial->write("Z\n\r");
  
  if (O2Serial->available()) {
    String O2Reading = O2Serial->readStringUntil('\n');
    float O2Percent = O2Reading.substring(26,32).toFloat();
  }
  
  if (CO2Serial->available()) {
    String CO2Reading = CO2Serial->readStringUntil('\n');
    float CO2Percent = CO2Reading.substring(2).toFloat()/1000;
  }

  float O2Ratio = abs(O2Setpoint - O2Percent);
  float CO2Ratio = abs(CO2Setpoint - CO2Percent);
}

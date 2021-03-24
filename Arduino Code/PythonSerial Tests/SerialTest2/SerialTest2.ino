/*
Code to test send_float function
Generates random numbers and sends them over serial

*/

void send_float (float arg)
{
  // get access to the float as a byte-array:
  byte * data = (byte *) &arg; 

  // write the data to the serial
  Serial.write (data, sizeof (arg));
  Serial.println();
}


void setup(){
  randomSeed(analogRead(0));  //Generate random number seed from unconnected pin
  Serial.begin(9600); //Begin Serial
}

void loop()
{
  int v1 = random(300); //Generate two random ints
  int v2 = random(300);
  float test = ((float) v1)/((float) v2);  // Then generate a random float

  Serial.print("m");  // Print test variable as string
  Serial.print(test,11);
  Serial.println();

  //print test variable as float
  Serial.print("d"); send_float(test);
  Serial.flush();
  //delay(1000);

}

int x;
float y;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 while (!Serial.available());
 y = Serial.readString().toFloat();
 Serial.print(y + 1);
 Serial.print(',');
 Serial.print(y*2);
}

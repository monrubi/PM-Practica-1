
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  int pot = analogRead(A0);
  int val = analogRead(A1);
  Serial.println(map(val, 0, 1023, 100, 0));
  Serial.println(map(pot, 0, 1023, 100, 0));

  if(val > pot){
    //Serial.println(11);
    digitalWrite(LED_BUILTIN, HIGH);  
  }else {
    //Serial.println(00);
    digitalWrite(LED_BUILTIN, LOW);
  }

  delay(800);
  

}

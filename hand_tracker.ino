#include <Servo.h>
Servo myservo; 

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt();
    if (angle > 0)
      myservo.write(angle);
  }
}

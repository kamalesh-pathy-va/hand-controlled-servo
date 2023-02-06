#include <Servo.h>
Servo myservo; 

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt();
    // parseInt will wait for sometime to see if there's any number in the buffer.
    // ending with a non-numarical value will return quickly, but converts the
    // non-numarical value to 0
    if (angle > 0) // so except for angle 0 rest of the angle it should turn the servo
    // this will prevent the servo resetting to 0
      myservo.write(angle);
  }
}

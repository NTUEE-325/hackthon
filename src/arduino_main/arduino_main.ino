#include <Arduino.h>
#include <Servo.h>

#define servo_pin01 3
#define servo_pin02 5
;
Servo servo01;
Servo servo02;

void setup(){
    servo01.attach(servo_pin01);
}

void loop(){
    servo01.write(0);
    delay(500);
    servo01.write(90);
    delay(500);
    servo01.write(180);
    delay(500);
}
;

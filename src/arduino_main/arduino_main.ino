#include <Arduino.h>
#include "MYservo.h"

void setup(){
    servoLR.attach(servo_pin_LR);
    servoUD.attach(servo_pin_UD);
}

void loop(){
}

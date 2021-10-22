#ifndef MYSERVO_H_INCLUDED
#define MYSERVO_H_INCLUDED

#include "Servo.h"

#define servo_pin_LR 3
#define servo_pin_UD 5
;

Servo servoLR;
Servo servoUD;


void servo_rotate(Servo myservo,const int theta){
    myservo.write(theta);
    delay(500);
}

#endif
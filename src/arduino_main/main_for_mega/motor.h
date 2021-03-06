#ifndef MOTOR.H
#define MOTOR.H

#define motor1Pin1  30     // IN1 on the ULN2003 driver
#define motor1Pin2  31      // IN2 on the ULN2003 driver
#define motor1Pin3  32     // IN3 on the ULN2003 driver
#define motor1Pin4  33     // IN4 on the ULN2003 driver
#define motor2Pin1  38      // IN1 on the ULN2003 driver
#define motor2Pin2  39      // IN2 on the ULN2003 driver
#define motor2Pin3  40     // IN3 on the ULN2003 driver
#define motor2Pin4  41     // IN4 on the ULN2003 driver



#include <AccelStepper.h>


#define MotorInterfaceType 8

int motorspeed = 500;

AccelStepper stepper1 = AccelStepper(MotorInterfaceType, motor1Pin1, motor1Pin3, motor1Pin2, motor1Pin4);
AccelStepper stepper2 = AccelStepper(MotorInterfaceType, motor2Pin1, motor2Pin3, motor2Pin2, motor2Pin4);


void setup_motor(){
  stepper1.setMaxSpeed(1000);
  stepper1.setCurrentPosition(0);
  stepper2.setMaxSpeed(1000);
  stepper2.setCurrentPosition(0);
}
int Return_steps2(int y){
  return y*100 ; //計算葉片上揚x度時，齒輪需要轉幾個step (4096 step =一圈)
}
void Motor_UD(int steps ){
  if ((steps-stepper2.currentPosition())<=0) stepper2.setSpeed(-1*motorspeed);
  else stepper2.setSpeed(motorspeed);
  stepper2.runSpeed();
  
}
int Return_steps1(int x){
  return x*100; //計算葉片上揚x度時，齒輪需要轉幾個step (4096 step =一圈)
}
void Motor_RL(int steps ){
  if ((steps-stepper1.currentPosition())<=0) stepper1.setSpeed(-1*motorspeed);
  else stepper1.setSpeed(motorspeed);
  stepper1.runSpeed();

}

#endif

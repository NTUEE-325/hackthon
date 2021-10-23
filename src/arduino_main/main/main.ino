/*#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

#include "bluetooth.h"
#include "lcd.h"
#include "motor.h"

#define GYMpin A1
#define NIGHTpin A2
#define STUDYpin A3
int xanglechange = 0;
int yanglechange = 0;
bool flag1 = true;
bool flag2 = true;
int steps1 = 0;
int steps2 = 0;
int laststeps1 =0;
int laststeps2 =0;
void setup()
{
  Serial.begin (9600);             // Serial Port begin
  setup_BT();
  setup_lcd();
  setup_motor();
  pinMode(GYMpin,OUTPUT);
  pinMode (NIGHTpin,OUTPUT);
  pinMode (STUDYpin, OUTPUT);
  //lcd.setCursor(0,3);
  //lcd.print("Happy Using!!!");
  //delay(5000);
  //lcd.setCursor(0,3);
  //lcd.print(clear_line);
}

void loop() {
  MODE mode = GETMODE();
  if (mode == DEFAULT_MODE){
    lcd.setCursor(0,1);
    //lcd.print(clear_line);
    //lcd.setCursor(0,2);
    lcd.print("DEFAULT_MODE        ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("default");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;
  }
  else if (mode == NIGHT_MODE){
    lcd.setCursor(0,1);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("NIGHT_MODE          ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("night");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 200);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;   
  }
  else if (mode == GYM_MODE){
    lcd.setCursor(0,1);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("GYM_MODE            ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("gym");
    analogWrite(GYMpin , 200);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;   
  }
  else if (mode == STUDY_MODE){
    lcd.setCursor(0,1);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("STUDY_MODE          ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("study");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 200);
    mode = NOTHING;
  }
  else if (mode == WIND_UPDOWN){
    lcd.setCursor(0,1);
    lcd.print(clear_line);
    lcd.setCursor(0,1);
    lcd.print("WIND_UPDOWN");
    xanglechange = countXAngle();
    lcd.setCursor(0,2);
    lcd.print("TURN_UD ");
    lcd.print(xanglechange);
    laststeps1 = steps1;
    steps1 = Return_steps1(xanglechange);
    if (stepper1.currentPosition() != steps1){
      Motor_UD(steps1 , laststeps1);
      if (stepper1.currentPosition() != steps1) flag1 = false;
      else flag1 = true;
    }
    mode = NOTHING; 
  }
  else if (mode == WIND_RIGHTLEFT){
    lcd.setCursor(0,1);
    lcd.print(clear_line);
    lcd.setCursor(0,1);
    lcd.print("WIND_RIGHTLEFT");
    yanglechange = countYAngle();
    lcd.setCursor(0,2);
    lcd.print("TURN_RL ");
    lcd.print(yanglechange);
    laststeps2 = steps2;
    steps2 = Return_steps2(yanglechange);
    if (stepper2.currentPosition() != steps2 ){
      Motor_UD(steps2 , laststeps2);
      if (stepper2.currentPosition() != steps2) flag2 = false;
      else flag2 = true;
    }
    mode = NOTHING;
  }
  else if (mode == WIND_STRONG){
    lcd.setCursor(0,2);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("WIND_STRONG         ");
    //Serial.write("wind_strong");
    lcd_windstrong();
    mode = NOTHING;
  }
  else if (mode == WIND_WEAK){
    lcd.setCursor(0,2);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("WIND_WEAK           ");
    //Serial.write("wind_weak");
    lcd_windsmall();
    mode = NOTHING;
  }
  else if(mode == NOTHING){
    lcd.setCursor(0,1);
    if (flag1 == false){
      Motor_UD(steps1 , laststeps1);
      if (stepper1.currentPosition() == steps1) flag1 = true;
    }
    if (flag2 == false){
      Motor_RL(steps2 , laststeps2);
      if (stepper2.currentPosition() == steps2) flag2 = true;
    }
    
    //lcd.print(clear_line);
  }
}*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

#include "bluetooth.h"
#include "lcd.h"
#include "motor.h"

#define GYMpin A1
#define NIGHTpin A2
#define STUDYpin A3
int xanglechange = 0;
int yanglechange = 0;
bool flag1 = true;
bool flag2 = true;
int steps1 = 0;
int steps2 = 0;
int laststeps1 =0;
int laststeps2 =0;
void setup()
{
  Serial.begin (9600);             // Serial Port begin
  setup_BT();
  setup_lcd();
  setup_motor();
  pinMode (GYMpin,OUTPUT);
  pinMode (NIGHTpin,OUTPUT);
  pinMode (STUDYpin, OUTPUT);
  //lcd.setCursor(0,3);
  //lcd.print("Happy Using!!!");
  //delay(5000);
  //lcd.setCursor(0,3);
  //lcd.print(clear_line);
}

void loop() {
  MODE mode = GETMODE();
  if (mode == DEFAULT_MODE){
    lcd.setCursor(0,0);
    //lcd.print(clear_line);
    //lcd.setCursor(0,2);
    lcd.print("DEFAULT_MODE        ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("default");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;
  }
  else if (mode == NIGHT_MODE){
    lcd.setCursor(0,0);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("NIGHT_MODE          ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("night");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 200);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;   
  }
  else if (mode == GYM_MODE){
    lcd.setCursor(0,0);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("GYM_MODE            ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("gym");
    analogWrite(GYMpin , 200);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 0);
    mode = NOTHING;   
  }
  else if (mode == STUDY_MODE){
    lcd.setCursor(0,0);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("STUDY_MODE          ");
    lcd.setCursor(0,2);
    lcd.print(clear_line);
    //Serial.write("study");
    analogWrite(GYMpin , 0);
    analogWrite(NIGHTpin , 0);
    analogWrite(STUDYpin , 200);
    mode = NOTHING;
  }
  else if (mode == WIND_UPDOWN){
    //lcd.setCursor(0,1);
    //lcd.print(clear_line);
    lcd.setCursor(0,1);
    lcd.print(clear_line);
    xanglechange = countXAngle();
    lcd.setCursor(0,1);
    lcd.print("TURN_UD ");
    lcd.print(xanglechange);
    //laststeps1 = steps1;
    Serial.write("steps:\n");
    Serial.println(steps1);
    steps1 = Return_steps1(xanglechange);
    if (stepper1.currentPosition() != steps1){
      Motor_UD(steps1);
      if (stepper1.currentPosition() != steps1) flag1 = false;
      else {
        flag1 = true;
        //stepper1.setCurrentPosition(0);
      }
    }
    mode = NOTHING; 
  }
  else if (mode == WIND_RIGHTLEFT){
    //lcd.setCursor(0,1);
    //lcd.print(clear_line);
    lcd.setCursor(0,1);
    lcd.print(clear_line);
    //lcd.print("WIND_RIGHTLEFT      ");
    yanglechange = countYAngle();
    lcd.setCursor(0,1);
    lcd.print("TURN_RL ");
    lcd.print(yanglechange);
    //laststeps2 = steps2;
    Serial.write("steps:\n");
    Serial.println(steps2);
    //Serial.println(laststeps2);
    steps2 = Return_steps2(yanglechange);
    if (stepper2.currentPosition() != steps2 ){
      Motor_UD(steps2);
      if (stepper2.currentPosition() != steps2) flag2 = false;
      else {
        flag2 = true;
        //stepper2.setCurrentPosition(0);
      }
    }
    mode = NOTHING;
  }
  else if (mode == WIND_STRONG){
    lcd.setCursor(0,2);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("WIND_STRONG         ");
    //Serial.write("wind_strong");
    lcd_windstrong();
    mode = NOTHING;
  }
  else if (mode == WIND_WEAK){
    lcd.setCursor(0,2);
    //lcd.print(clear_line);
    //lcd.setCursor(0,1);
    lcd.print("WIND_WEAK           ");
    //Serial.write("wind_weak");
    lcd_windsmall();
    mode = NOTHING;
  }
  else{
    if (flag1 == false){
      Motor_UD(steps1);
      if (stepper1.currentPosition() == steps1){
        lcd.setCursor(0,1);
        lcd.print(clear_line);
        flag1 = true;
        //stepper1.setCurrentPosition(0);
      }
    }
    if (flag2 == false){
      Motor_RL(steps2);
      if (stepper2.currentPosition() == steps2) {
        lcd.setCursor(0,1);
        lcd.print(clear_line);
        flag2 = true;
        //stepper2.setCurrentPosition(0);
      }
    }
    
    //lcd.print(clear_line);
  }
}
 

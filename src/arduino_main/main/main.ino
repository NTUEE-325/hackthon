#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

#include "bluetooth.h"
#include "lcd.h"
#include "motor.h"

#define GYMpin A1
#define NIGHTpin A2
#define STUDYpin A3
int anglechange = 0;
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
    anglechange = countXAngle();
    lcd.setCursor(0,2);
    lcd.print("TURN_UD");
    lcd.print(anglechange);
    Motor_UD(anglechange);
    mode = NOTHING; 
  }
  else if (mode == WIND_RIGHTLEFT){
    lcd.setCursor(0,1);
    lcd.print(clear_line);
    lcd.setCursor(0,1);
    lcd.print("WIND_RIGHTLEFT");
    anglechange = countYAngle();
    lcd.setCursor(0,2);
    lcd.print("TURN_RL");
    lcd.print(anglechange);
    Motor_RL(anglechange);
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
  else {
    lcd.setCursor(0,1);
    //lcd.print(clear_line);
  }
}
  /*  
  switch(mode){
    case DEFAULT_MODE:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("DEFAULT_MODE");
      digitalWrite(GYMpin , LOW);
      digitalWrite(NIGHTpin , LOW);
      digitalWrite(STUDYpin , LOW);
    case NIGHT_MODE:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("NIGHT_MODE");
      digitalWrite(GYMpin , LOW);
      digitalWrite(NIGHTpin , HIGH);
      digitalWrite(STUDYpin , LOW);
    case GYM_MODE:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("GYM_MODE");
      digitalWrite(GYMpin , HIGH);
      digitalWrite(NIGHTpin , LOW);
      digitalWrite(STUDYpin , LOW);
    case STUDY_MODE:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("STUDY_MODE");
      digitalWrite(GYMpin , LOW);
      digitalWrite(NIGHTpin , LOW);
      digitalWrite(STUDYpin , HIGH);
    case WIND_UPDOWN:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("WIND_UPDOWN");
      anglechange = countXAngle();
      Motor_UD(anglechange); 
    case WIND_RIGHTLEFT:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("WIND_RIGHTLEFT");
      anglechange = countYAngle();
      MOTOR_RL(anglechange);
    case WIND_STRONG:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("WIND_STRONG");
      lcd_windstrong();
    case WIND_WEAK:
      lcd.setCursor(0,0);
      lcd.print(clear_line);
      lcd.print("WIND_WEAK");
      lcd_windsmall();
    default:
      break;
  }
  */

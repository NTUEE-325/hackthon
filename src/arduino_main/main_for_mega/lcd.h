#ifndef LCD.H
#define LCD.H

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 20, 4);
extern String clear_line = "                    ";
int times = 3;

void setup_lcd(){
  Wire.begin();
  lcd.begin();
  // Turn on the blacklight and print a message.
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("PixArt-02");
  lcd.setCursor(0,3);
  lcd.print("flow:# # #");
  
}

void lcd_windstrong(){
  if (times<5){
    lcd.setCursor(5+2*times,3);
    lcd.print("# ");
    times++;
  }
}

void lcd_windsmall(){
  if (times>0) {
    lcd.setCursor(5+2*(times-1),3);
    lcd.print("  ");
    times--;
  }
}

#endif

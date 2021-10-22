#ifndef BLUETOOTH.H
#define BLUETOOTH.H

#include <SoftwareSerial.h>
#define TX_PIN 2 
#define RX_PIN 3 
SoftwareSerial BT(RX_PIN , TX_PIN);

char message;
int angle=0;
int third=0;
int second=0;
int first=0;
int a=0; //use in countXAngle(),countYAngle(),


enum MODE{
  NOTHING,
  DEFAULT_MODE,
  NIGHT_MODE,
  GYM_MODE,
  STUDY_MODE,
  WIND_UPDOWN,
  WIND_RIGHTLEFT,
  WIND_STRONG,
  WIND_WEAK
};

void setup_BT(){
  BT.begin(9600);
}

int countXAngle(){
  third = BT.read()-48;
  second = BT.read()-48;
  first = BT.read()-48;
  angle = third*100+second*10+first;
  a = angle-90;
  return a;
}


int countYAngle(){
  third = BT.read()-48;
  second = BT.read()-48;
  first = BT.read()-48;
  angle = third*100+second*10+first;
  a = angle-90;
  return a;
}

MODE GETMODE(){
  if (BT.available()){
    message = BT.read();
    if (message=='d') return DEFAULT_MODE;
    else if (message == 'n') return NIGHT_MODE;
    else if (message == 'g') return GYM_MODE;
    else if (message == 's') return STUDY_MODE;
    else if (message == 'x') return WIND_UPDOWN;
    else if (message == 'y') return WIND_RIGHTLEFT;
    else if (message == '+') return WIND_STRONG;
    else if (message == '-') return WIND_WEAK;
    else return NOTHING;
    delay(500);
  }
}

#endif

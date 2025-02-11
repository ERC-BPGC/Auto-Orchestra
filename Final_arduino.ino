#include <Servo.h>
int ogserv;
Servo kservo[25];
int fa(int f){
  return(f==1?70:(f==0?0:90));
  }
void servocom(int x, int lor){
  int ang = lor==1?40:140;
  if(ogserv!=x)
   kservo[ogserv-1].write(90);
kservo[x-1].write(ang);
ogserv = x;
}  
void flute(int f1, int f2, int f3, int f4, int f5, int f6){
   kservo[19].write(fa(f1));
   kservo[20].write(fa(f2));
   kservo[21].write(fa(f3));
   kservo[22].write(fa(f4));
   kservo[23].write(fa(f5));
   kservo[24].write(fa(f6));  
}
 

void setup() {
  Serial.begin(9600);
int pin = 22;
int servonum=0;
while(servonum<=24){
  kservo[servonum].attach(pin);
  kservo[servonum].write(90);
  delay(100);
  servonum++;
  pin++;
}
}


void loop() {
  String myString= Serial.readStringUntil('\n');
//string format  is servonumber|sense of rotation - 1 for ACW and 0 for CW|6 digitsfor flute holes, 0 for open, 1 for half open, 2 fully closed|       eg. 121012121
//format for servo numbers, is 01 for first servo ond 19 for the last.
  
 String subString1 = myString.substring(0, 2);
 String subString2 = myString.substring(2, 3);
int x;
int lor;
x = subString1.toInt(); // servo1
lor = subString2.toInt(); //cw or acw
servocom(x,lor);
flute(myString[3]-48,myString[4]-48,myString[5]-48,myString[6]-48,myString[7]-48,myString[8]-48);
}
#include <Servo.h>
Servo kservo[19];
void servocom(int x, int y, int lor){
  int ang = lor==1?40:140;
 kservo[x-1].write(ang);
 delay(y);
 kservo[x-1].write(90); 
  }  
  

void setup() {
  Serial.begin(9600);
int pin = 22;
int servonum=0;
while(servonum<=18){
  kservo[servonum].attach(pin);
  kservo[servonum].write(90);
  delay(100);
  servonum++;
  pin++;
}
}


void loop() {
  String myString= Serial.readStringUntil('\n');
//string format  is servonumber|servonumber|delay|1 for ACW and 0 for CW   eg. 0110001
//format for servo numbers, is 01 for first servo of first driver and 11 for first servo of second driver,
//for using only one servo at a time give 00.
  
 String subString1 = myString.substring(0, 2);
  //Serial.println(subString1);  
 String subString2 = myString.substring(2,6);
  //Serial.println(subString2);  
 String subString4 = myString.substring(6, 7);
   //Serial.println(subString4); 
 
int x;
int y;
int lor;
x = subString1.toInt(); // servo1
y = subString2.toInt(); // delay
lor = subString4.toInt(); //cw or acw
servocom(x,y,lor);
}

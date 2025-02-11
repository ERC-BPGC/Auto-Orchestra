#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create an instance of the PCA9685 driver
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41);

// Servo settings
#define SERVOMIN 150  // Minimum pulse length count (approx 0°)
#define SERVOMAX 600  // Maximum pulse length count (approx 180°)

// Function to convert angle to pulse length

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}
void servocom(int x, int y, int lor){
  int ang = lor==1?25:155;
  //digitalWrite(x+30,HIGH);
  if(x>11)
   pwm2.setPWM(x-11, 0, angleToPulse(ang));
 else
  pwm1.setPWM(x-1, 0, angleToPulse(ang));
 delay(y);
   if(x>11)
   pwm2.setPWM(x-11, 0, angleToPulse(90));
 else
  pwm1.setPWM(x-1, 0, angleToPulse(90));
   digitalWrite(x+30,LOW);
  }
void flute(int f1, int f2, int f3, int f4, int f5, int f6, int del){
   pwm2.setPWM(4, 0, angleToPulse(f1-48==0?90:135));
    pwm2.setPWM(5, 0, angleToPulse(f2-48==0?90:135));
     pwm2.setPWM(6, 0, angleToPulse(f3-48==0?90:135));
      pwm2.setPWM(7, 0, angleToPulse(f4-48==0?90:135));
       pwm2.setPWM(8, 0, angleToPulse(f5-48==0?90:135));
        pwm2.setPWM(9, 0, angleToPulse(f6-48==0?90:135));
        delay(del);
        pwm2.setPWM(4, 0, angleToPulse(90));
    pwm2.setPWM(5, 0, angleToPulse(90));
     pwm2.setPWM(6, 0, angleToPulse(90));
      pwm2.setPWM(7, 0, angleToPulse(90));
       pwm2.setPWM(8, 0, angleToPulse(90));
        pwm2.setPWM(9, 0, angleToPulse(90));
}


void setup() {
  int k = 10;
  pwm1.begin();
  pwm1.setPWMFreq(50); 
   pwm2.begin();
  pwm2.setPWMFreq(50); // Set frequency to 50 Hz

Serial.begin(9600);
while(k>=0){ 
  //pinMode(k+21,OUTPUT); // SETTING PINS FOR CORRESPONDING leds 21,22,23.... &31,32,33... 
  //pinMode(k+31,OUTPUT);
  // pwm1.setPWM(k, 0, angleToPulse(90));// to bring all servos to normal position at the very start
    //pwm2.setPWM(k, 0, angleToPulse(90));
    k--;
    //delay(1000);
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
int lor, del;
x = subString1.toInt(); // servo1
y = subString2.toInt(); // delay
lor = subString4.toInt(); //cw or acw
del = (myString.substring(13,17)).toInt();
servocom(x,y,lor);
flute(myString[7],myString[8],myString[9],myString[10],myString[11],myString[12],del);
}

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Servo.h>
 Servo S1;
 Servo S2;
 Servo S3; 
// Create an instance of the PCA9685 driver
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);


// Servo settings
#define SERVOMIN 150  // Minimum pulse length count (approx 0°)
#define SERVOMAX 600  // Maximum pulse length count (approx 180°)

// Function to convert angle to pulse length
// map(value, fromLow, fromHigh, toLow, toHigh)
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void servocom(int x, int y, int lor){
  int ang = lor==0 ? 45 : 135; // using terinary operator
  // Equivalent form of the above line
  // int ang;
  // if (lor == 0) {
  //   ang = 45;
  // }
  // else {
  //   ang = 135;
  // }

  digitalWrite(x+20,HIGH);
  if(x>0 && x<=16)
    pwm1.setPWM(x-1, 0, angleToPulse(ang));// Servo on channel no., 0, Moving angle
   else if(x==17)
   S1.write(ang); 
   else if(x==18)
   S2.write(ang); 
   else if(x==19)
   S3.write(ang); 
  delay(y);
  if(x>0 && x<=16)
    pwm1.setPWM(x-1, 0, angleToPulse(90));// Servo on channel no., 0, Moving angle
   else if(x==17)
   S1.write(90); 
   else if(x==18)
   S2.write(90); 
   else if(x==19)
   S3.write(90); 
    

}
void setup() {
  int k = 15;
  pwm1.begin();
  pwm1.setPWMFreq(50); 

Serial.begin(9600);
while(k>=0){ 
//  pinMode(,OUTPUT); // SETTING PINS FOR CORRESPONDING leds 21,22,23.... &31,32,33... 
    pwm1.setPWM(k, 0, angleToPulse(90));// to bring all servos to normal position at the very start
    k--;
    delay(100);
}
S1.attach(9);
S1.write(90);
S2.attach(10);
S2.write(90);
S3.attach(11);
S3.write(90);

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

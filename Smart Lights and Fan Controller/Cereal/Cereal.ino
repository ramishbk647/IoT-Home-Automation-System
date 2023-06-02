#include <Servo.h>

Servo myservo;
unsigned int pinStatus = 0;
const int ldrPin = A0;
const int TempPin = A2;

boolean lampOn = false;
boolean fanOn = false;
boolean autoLampOn = false;
boolean autoFanOn = true;
boolean autoFan1On = true;
const long eventTime_Tem = 4250;
unsigned long previousTime_Tem = 0;
int x;
unsigned temptot = 0;





void setup()
{
  Serial.begin(9600);
  analogReference(INTERNAL);
  pinMode(8,OUTPUT);//Bulb
  pinMode(11,OUTPUT);//Case Fan
  pinMode(10,OUTPUT);//CPU Fan
  pinMode(ldrPin,INPUT);//LDR Sensor
  pinMode(TempPin,INPUT);//LDR Sensor
  myservo.attach(9);//Door Lock

  digitalWrite(8, LOW);
  digitalWrite(11, LOW);
  digitalWrite(10, HIGH);
  myservo.write(0);
}

bool inRange(int val, int minimum, int maximum)
{
  return ((minimum <= val) && (val <= maximum));
}

void loop()
{
  int x;
  unsigned long currentTime = millis();
  unsigned long temptot = 0;
  int LDRVal = analogRead(ldrPin);
  int LMVal = analogRead(TempPin);

  for(x=0; x<100 ; x++)
  {
    temptot += LMVal;
  }
  float sensorValue = temptot/100;
  float voltage = sensorValue * (1100 / 1023);
  float temperature = voltage*0.1;

  String sensordata = String(LDRVal) + "," + String(temperature);

  if(currentTime-previousTime_Tem >=eventTime_Tem)
  {
    
   
        Serial.println(sensordata); 
      
    previousTime_Tem = currentTime;

        
  }
  
  
  if (Serial.available() > 0)
{
  
  // parse incoming Serial data to integer
  pinStatus = Serial.parseInt();
  switch (pinStatus)
  {
    case 1:
    digitalWrite(10, HIGH);
    autoFanOn = false;
    break;
    case 2:
    digitalWrite(10, LOW);
    autoFanOn = false;
    break;
    case 3:
    digitalWrite(11, HIGH);
    autoFan1On = false;
    break;
    case 4:
    digitalWrite(11, LOW);
    autoFan1On = false;
    break;
    case 5:
    digitalWrite(8, HIGH);
    autoLampOn = false;
    break;
    case 6:
    digitalWrite(8, LOW);
    autoLampOn = false;
    break;
    case 7:
    myservo.write(180);
    break;
    case 8:
    myservo.write(0);
    break;
    case 9:
    myservo.write(180);
    autoLampOn = true;
    break;
    case 10:
    myservo.write(0);
    autoLampOn = false;
    break;
    default:
    break;
    }
  }
   if (autoLampOn == true)
  {
    if (LDRVal <=270)
      {
        delay(1000);
        digitalWrite(8, HIGH);
        
      }
      else{
        delay(1000);
        digitalWrite(8, LOW);
  }

  }
}

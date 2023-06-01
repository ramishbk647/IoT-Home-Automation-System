#include <Servo.h>

Servo myservo;  // create servo object to control a servo

const int PIR_SENSOR_OUTPUT_PIN = 4;  // PIR sensor O/P pin 
int warm_up;
const int trigPin = 10;
const int echoPin = 11;
int threshold = 12;
long duration;
int distance;

void setup() {
  pinMode(PIR_SENSOR_OUTPUT_PIN, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(2, OUTPUT); // 
  Serial.begin(9600); // Define baud rate for serial communication 
  delay(10000); // Power On Warm Up Delay 
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  int sensor_output;
  sensor_output = digitalRead(PIR_SENSOR_OUTPUT_PIN);
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  Serial.println(distance);
  Serial.println(sensor_output);
  if( sensor_output == LOW || distance > threshold)
  {
    if( warm_up == 1 )
    {
      warm_up = 0;
      delay(2000);
    }
    digitalWrite(2, LOW);
    Serial.println("No object in sight");
    Serial.println("Close");
    myservo.write(0);  // moves the servo to 0 degrees
    delay(1000);
  }
  else 
  {
    digitalWrite(2, HIGH);
    Serial.println("Object detected");  
    Serial.println("Open");  
    warm_up = 1;
    myservo.write(90); // moves the servo to 90 degrees
    delay(1000);
    
  }  
} 

#include <Servo.h>
int servoPin = 3;
int ledPin = 4;
int tempSensorPin = A2;
const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;
Servo Servo1;

void setup() {
	// put your setup code here, to run once:
	Servo1.attach(servoPin);
	pinMode(4, OUTPUT);
	Serial.begin(9600);
}

void loop() {
	// detect pet pressence
	// Get the voltage reading from the TMP36
	int reading = analogRead(sensorPin);
	// Convert that reading into voltage
	// Replace 5.0 with 3.3, if you are using a 3.3V Arduino
	float voltage = reading * (5.0 / 1024.0);
	// Convert the voltage into the temperature in Celsius
	float temperatureC = (voltage - 0.5) * 100;
	// Print the temperature in Celsius
	Serial.print("Temperature: ");
	Serial.print(temperatureC);
	Serial.print("\xC2\xB0"); // shows degree symbol
	Serial.print("C | ");
	delay(1000); // wait a second between readings
	
	if(temperatureC < 38.0){
		//dispense food
		Servo1.write(0);
		delay(1000);
		Servo1.write(90);
		Serial.println("Dispense Sucessfully!");
		//check availability of food
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
		distance = duration * 0.034 / 2;
		// Prints the distance on the Serial Monitor
		Serial.print("Distance: ");
		Serial.println(distance);
		delay(3000);
		//turn LED on to indicate that food is running out
		if(distance > 20){
			digitalWrite(ledPin, HIGH);
		}else{
			digitalWrite(ledPin, LOW);
		}
	}
}
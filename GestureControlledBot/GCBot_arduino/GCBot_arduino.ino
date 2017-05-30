#include <SoftwareSerial.h>


/**
 * Connections.
 * The Rx of the bluetooth Module HC-05 should be connected to pin 11.
 * The Tx of HC-05 should be connected to pin 10.
 * Pin 2,3,4,5,7,8 should be connected to the corresponding pin on the motor driver ciruit
 * The motor fited on the left should be connected to 2,3,4 pins 
 * The motor fited on the right should be connected to 5,7,8 pins
 */

 
// Motor 1 control pins defined here Left Motor
#define  M1_IN1   2
#define  M1_IN2   4
#define  M1_EN    3
// Motor 2 control pins defined here Right Motor
#define  M2_IN1   7
#define  M2_IN2   8
#define  M2_EN    5


SoftwareSerial terminal(10,11);// 10 -- Rx , 11 -- Tx of Bluetooth Module
char direction;
void setup()
{
  pinMode(M1_IN1, OUTPUT);   
  pinMode(M1_IN2, OUTPUT);   
  pinMode(M1_EN, OUTPUT);   
  pinMode(M2_IN1, OUTPUT);   
  pinMode(M2_IN2, OUTPUT);   
  pinMode(M2_EN, OUTPUT);   
  
  terminal.begin(9600);
  terminal.println("Connected and initiated");

  Serial.begin(9600);
  Serial.println("Connected and initiated");
}

void loop()
{
  if(terminal.available())
  {
    direction = terminal.read();

    if( direction == 'W')
    {
      digitalWrite(M1_IN1, HIGH);
      digitalWrite(M1_IN2, LOW);
      digitalWrite(M1_EN, HIGH);
      digitalWrite(M2_IN1, HIGH);
      digitalWrite(M2_IN2, LOW);
      digitalWrite(M2_EN, HIGH);
      Serial.println("Forward");      
    }

    if( direction == 'S')
    {
      digitalWrite(M1_IN1, LOW);
      digitalWrite(M1_IN2, HIGH);
      digitalWrite(M1_EN, HIGH);
      digitalWrite(M2_IN1, LOW);
      digitalWrite(M2_IN2, HIGH);
      digitalWrite(M2_EN, LOW);
      Serial.println("Backward");      
    }

    if( direction == 'A')
    {
      digitalWrite(M1_IN1, LOW);
      digitalWrite(M1_IN2, HIGH);
      digitalWrite(M1_EN, HIGH);
      digitalWrite(M2_IN1, HIGH);
      digitalWrite(M2_IN2, LOW);
      digitalWrite(M2_EN, HIGH);
      Serial.println("Left");      
    }

    if( direction == 'D')
    {
      digitalWrite(M1_IN1, HIGH);
      digitalWrite(M1_IN2, LOW);
      digitalWrite(M1_EN, HIGH);
      digitalWrite(M2_IN1, LOW);
      digitalWrite(M2_IN2, HIGH);
      digitalWrite(M2_EN, HIGH);
      Serial.println("Right");      
    }
  }

  else
  {
      digitalWrite(M1_IN1, LOW);
      digitalWrite(M1_IN2, LOW);
      digitalWrite(M1_EN, LOW);
      digitalWrite(M2_IN1, LOW);
      digitalWrite(M2_IN2, LOW);
      digitalWrite(M2_EN, LOW);
      Serial.println("Stop");      
  }

}

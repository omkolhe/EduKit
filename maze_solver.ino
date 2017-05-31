// maze solver robot//
//defining input sensors//
#define LS 2
#define RS 3
#define CS 4


//defining output for motors//
#define LM1 5 
#define LM2 6
#define RM1 7
#define RM2 8


//#include <ArduinoRobot.h>

void setup() {
  pinMode(LS, INPUT);
  pinMode(RS, INPUT);
  pinMode(CS,INPUT);
  pinMode(LM1, OUTPUT);
  pinMode(LM2, OUTPUT);
  pinMode(RM1, OUTPUT);
  pinMode(RM2, OUTPUT);
  //Robot.begin();

}

void loop()
{
 
   if(digitalRead(LS) && digitalRead(RS) && !(digitalRead(CS)))     // Move Forward
  {
    digitalWrite(LM1, HIGH);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
  }
  
  else if(digitalRead(LS)==1&& digitalRead(CS)==0 && digitalRead(RS)==0)     // Turn right
  {
    digitalWrite(LM1, HIGH);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, LOW);
    digitalWrite(RM2, LOW);
  }
  
  else if(digitalRead(LS)==0 && (digitalRead(CS)==0) &&digitalRead(RS)==1)     // turn left
  {
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
  }
  
//  else if( digitalRead(LS)==1 &&  (digitalWrite(CS==0)) && digitalRead(RS)==1 )     // stop
//  {
//    digitalWrite(LM1, LOW);
//    digitalWrite(LM2, LOW);
//    digitalWrite(RM1, LOW);
//    digitalWrite(RM2, LOW);
//  }
  else if(digitalRead(LS)==1 &&digitalRead(CS)==1 && digitalRead(RS)==1) //180 turn through right
  {
   //Robot.turn(180);
   digitalWrite(LM1, HIGH);
   digitalWrite(LM2,LOW);
   digitalWrite(RM1,LOW);
   digitalWrite(RM2,LOW);  }
  
  else if(digitalRead(LS)==0 && digitalRead(CS)==0 && digitalRead(RS)==0)   // always left
  {
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
    }

}

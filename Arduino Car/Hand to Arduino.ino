int left_motor = 12;
int right_motor = 13;
int speed = 255;
int stop = 0;
String action;

void moveForward(int);
void moveLeft(int);
void moveRight(int);
void stopMoving();

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  analogWrite(left_motor, 0);
  analogWrite(right_motor, 0);
}

void loop() {
  
  while(!Serial.available());
  action = Serial.readString();
  char c = action[0];
  
  if(c == 'w'){
    moveForward(speed);
  }
  else if(c == 'a') {
    moveLeft(speed);
  }
  else if(c == 'd') {
    moveRight(speed);
  }
  else if (c == 's'){
    stopMoving(); // If you've L298N, implement moveBackward
  }
  else{
    stopMoving();
  }
}

void moveForward(int speed = 255) {
  analogWrite(left_motor, speed);
  analogWrite(right_motor, speed);
}

void moveLeft(int speed = 255) {
  analogWrite(left_motor, stop);
  analogWrite(right_motor, speed);
}

void moveRight(int speed = 255) {
  analogWrite(left_motor, speed);
  analogWrite(right_motor, stop);
}

void stopMoving() {
  analogWrite(left_motor, stop);
  analogWrite(right_motor, stop);
}

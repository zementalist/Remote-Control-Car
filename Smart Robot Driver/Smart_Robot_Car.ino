                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   int left_motor = 12;
int right_motor = 13;
int speed = 255;
int stop = 0;

enum Direction {
  left, right
};
Direction direction_to_turn = left;

int trigger = 5;
int echo = 6;
int threshold = 20; // 20 CM to decide that there is an object
const float velocity = 0.034; // speed of sound centimeter/microsecond

int ir = 31;
bool prestate_object_detected = false;
bool object_detected = false;

void moveForward(int);
void turnLeft(int);
void turnRight(int);
void stopMoving();
void turn(int);

void emitWave();
float detectObjects();
bool isObjectNear(int);

void emitWave() {
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
}

float detectObjects() {
  emitWave();
  int duration = pulseIn(echo, HIGH);
  float distance = velocity * duration / 2.0;
  return distance;
}

bool isObjectNear(int threshold=threshold) {
  int frontal_distance = (int)abs(detectObjects());
  Serial.println(frontal_distance);
  return frontal_distance <= threshold && frontal_distance != 0;
}

void moveForward(int speed = speed) {
  analogWrite(left_motor, speed);
  analogWrite(right_motor, speed);
}

void turnLeft(int speed = speed) {
  analogWrite(left_motor, stop);
  analogWrite(right_motor, speed);
}

void turnRight(int speed = speed) {
  analogWrite(left_motor, speed);
  analogWrite(right_motor, stop);
}

void turn() {
  if(direction_to_turn == left)
      turnLeft();
  else
      turnRight();
}

void stopMoving() {
  analogWrite(left_motor, stop);
  analogWrite(right_motor, stop);
}

void setup() {
  Serial.begin(115200);
  stopMoving();

  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  // clear any emitted wave
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);

  pinMode(ir, INPUT);
}

void loop() {
//  bool object_is_near = isObjectNear(threshold);
  int path_is_clear = digitalRead(ir);
  object_detected = ! path_is_clear;
  if (object_detected && !prestate_object_detected) {
    stopMoving();
    delay(500);
    prestate_object_detected = object_detected;
    direction_to_turn = direction_to_turn == left ? right : left;
    Serial.println("OD");
  }
  else if(prestate_object_detected && object_detected){
    turn();
    Serial.println("POD & OD");
  }
  else if(prestate_object_detected && ! object_detected) {
    delay(1000);
    stopMoving();
    delay(500);
    prestate_object_detected = false;
    Serial.println("POD");
  }

  if(!object_detected && !prestate_object_detected){
      moveForward();
      Serial.println("NOTHING");
  }
  
}

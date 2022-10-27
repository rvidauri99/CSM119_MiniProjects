#include <Arduino_LSM6DS3.h>

int unit = 200;
void dot(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(unit);
  digitalWrite(LED_BUILTIN, LOW);
  delay(unit);
}
void dash(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(unit*3);
  digitalWrite(LED_BUILTIN, LOW);
  delay(unit);
}
void space_letters(){
  delay(unit*3);
}
void space_words(){
  delay(unit*7);
}

float ax, ay, az, gx, gy, gz;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  delay(2000);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

// the loop function runs over and over again forever
void loop() {
  /*----------------------PART 1----------------------*/
  //H
  dot();
  dot();
  dot();
  dot();
  space_letters();
  //E
  dot();
  space_letters();
  //L
  dot();
  dash();
  dot();
  dot();
  space_letters();
  //L
  dot();
  dash();
  dot();
  dot();
  space_letters();
  //O
  dash();
  dash();
  dash();
  space_letters();

  //SPACE
  space_words();

  //I
  dot();
  dot();
  space_letters();
  //M
  dash();
  dash();
  space_letters();
  //U
  dot();
  dot();
  dash();
  space_letters();

  /*----------------------PART 2----------------------*/
  // if (IMU.accelerationAvailable()) {
  //   IMU.readAcceleration(ax, ay, az);
  // }
  // if (IMU.gyroscopeAvailable()) {
  //   IMU.readGyroscope(gx, gy, gz);
  // }

  // Serial.print("ax: ");
  // Serial.print(ax);
  // Serial.print(" , ay: ");
  // Serial.print(ay);
  // Serial.print(" , az: ");
  // Serial.print(az);
  // Serial.print(" , gx: ");
  // Serial.print(gx);
  // Serial.print(" , gy: ");
  // Serial.print(gy);
  // Serial.print(" , gz: ");
  // Serial.println(gz);

  delay(1000);
}
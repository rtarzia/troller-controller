#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define GO_PIN     21
#define RIGHT_PIN  22
#define LEFT_PIN   23
#define POT_PIN    13

BluetoothSerial SerialBT;

int go_lastState = HIGH, speed_lastState = 0;
int go_currentState, right_currentState, left_currentState, speed_currentState;

void setup() {
  Serial.begin(9600);
  pinMode(GO_PIN, INPUT_PULLUP);
  pinMode(RIGHT_PIN, INPUT_PULLUP);
  pinMode(LEFT_PIN, INPUT_PULLUP);
  SerialBT.begin("ESP32test");
  Serial.println("device started");
}

void loop() {

  if (Serial.available()) {
    char buf[128] = {};
    char* bufptr = buf;
    while(Serial.available()) {
      *bufptr = Serial.read();
      bufptr++;
    }
    SerialBT.print(buf);
  }
  
  go_currentState = digitalRead(GO_PIN);
  int pot_currentState = analogRead(POT_PIN);
  int speed_currentState = (int)((pot_currentState * 100) / 4095);

  if (abs(speed_currentState - speed_lastState) > 2) {
    if (go_currentState == LOW) {
      Serial.println("change speed");
      char buf[4] = {};
      sprintf(buf, "p%d", speed_currentState);
      Serial.println(buf);
      SerialBT.print(buf);
      speed_lastState = speed_currentState;
    }
  }

  if (go_currentState != go_lastState) {
    if(go_currentState == HIGH) {
      Serial.println("stop go");
      go_lastState = HIGH;
      SerialBT.print("p0");
    }
  
    else if(go_currentState == LOW) {
      Serial.println("go");
      go_lastState = LOW;
      char buf[4] = {};
      sprintf(buf, "p%d", speed_currentState);
      Serial.println(buf);
      SerialBT.print(buf);
      speed_lastState = speed_currentState;
    }
  }

  right_currentState = digitalRead(RIGHT_PIN);
  left_currentState = digitalRead(LEFT_PIN);

  if (right_currentState == LOW && left_currentState == HIGH) {
    Serial.println("right");
    SerialBT.print("sr");
  } else if (right_currentState == HIGH && left_currentState == LOW) {
    Serial.println("left");
    SerialBT.print("sl");
  }

  delay(20);
}
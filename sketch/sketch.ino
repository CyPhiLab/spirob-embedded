
#include <Arduino_RouterBridge.h>

const int sensorPin1 = A0;
const int sensorPin2 = A1;
const int sensorPin3 = A2;
const int sensorPin4 = A3;

int get_sensor1() {
    return analogRead(sensorPin1);
}

int get_sensor2() {
    return analogRead(sensorPin2);
}

int get_sensor3() {
    return analogRead(sensorPin3);
}

int get_sensor4() {
    return analogRead(sensorPin4);
}

void setup() {
    analogReadResolution(10);

    Bridge.begin();

    Bridge.provide_safe("get_sensor1", get_sensor1);
    Bridge.provide_safe("get_sensor2", get_sensor2);
    Bridge.provide_safe("get_sensor3", get_sensor3);
    Bridge.provide_safe("get_sensor4", get_sensor4);
}

void loop() {
    delay(10);
}

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "ServoHandler.h"

ServoHandler servoHandler;

void setup() {
    Serial.begin(115200);
    Serial.println("Alternate Servo Test");
    servoHandler.setupServos();
}

void loop() {
    // Define the positions for the servos to move to
    std::vector<int> positionsToMax = {180, 180, 180};
    std::vector<int> positionsToMin = {0, 0, 0};

    // Move servos to maximum positions
    Serial.println("\nStage1");
    servoHandler.servoSetPosition(positionsToMax);
    Serial.println("Stage2");
    delay(100);
    Serial.println("Stage3");

    // Move servos back to minimum positions
    Serial.println("Stage4");

    servoHandler.servoSetPosition(positionsToMin);
    Serial.println("Stage5");

    delay(100);
    Serial.println("Stage6");

}
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "ServoHandler.h"

const int defaultPos[3] = {0, 0, 0};


ServoHandler* servoHandler = new ServoHandler(defaultPos);

void setup() {
    Serial.begin(115200);
    Serial.println("Alternate Servo Test");
    servoHandler->setupServos();
    // servoHandler.test();
    // Serial.println("Alternate Servo Test");
}

void loop() {
    // Define the positions for the servos to move to
    std::vector<int> positionsToMax = {180, 180, 180};
    std::vector<int> positionsToMin = {0, 0, 0};

    servoHandler->servoSetPosition(positionsToMax, "To max");
    Serial.println("Break...");
    delay(5000);

    servoHandler->servoSetPosition(positionsToMin, "To low");
    Serial.println("Break...");
    delay(5000);


    // Move servos to maximum positions
    // Serial.println("\nStage1");
    // servoHandler.servoSetPosition(positionsToMax);
    // Serial.println("Stage2");
    // delay(5000);
    // Serial.println("Stage3");

    // // Move servos back to minimum positions
    // Serial.println("Stage4");

    // servoHandler.servoSetPosition(positionsToMin);
    // Serial.println("Stage5");

    // delay(100);
    // Serial.println("Stage6");

}

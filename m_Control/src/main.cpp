#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "ServoHandler.h"

const int defaultPos[5] = {180, 180, 90, 0, 0};


ServoHandler* servoHandler = new ServoHandler(defaultPos);

void setup() {
    Serial.begin(115200);
    Serial.println("Alternate Servo Test");
    servoHandler->setupServos();
    // servoHandler.test();
    // Serial.println("Alternate Servo Test");
}

void loop() {
    Serial.println("\n\n\n STARTE \n\n\n");
    // servoHandler->robotPickUp();

    // TEST CLAWS
    std::vector<int> open = {180, 180, 90, 90, 90};
    servoHandler->servoSetPosition(open, "Rotate to object position");
    delay(1000);
    Serial.println("\n\nCounter Clockwise\n\n");

    std::vector<int> close = {180, 180, 90, 190, 95};
    servoHandler->servoSetPosition(close, "Rotate to object position");
    delay(1000);
    Serial.println("\n\nClockwise\n\n");

    std::vector<int> stop = {180, 180, 90, 180, 90};
    servoHandler->servoSetPosition(stop, "Rotate to object position");
    delay(1000);
    Serial.println("\n\nCounter Clockwise\n\n");

    // TEST CLAWS
    std::vector<int> back = {180, 180, 90, 10, 85};
    servoHandler->servoSetPosition(back, "Rotate to object position");
    delay(1000);
    Serial.println("\n\nBack\n\n");

    // std::vector<int> close = {180, 180, 90, 180, 80};
    // servoHandler->servoSetPosition(close, "Rotate to object position");
    // delay(500);
    // Serial.println("\n\nTEST END\n\n");

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

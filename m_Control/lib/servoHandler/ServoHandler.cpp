#include "ServoHandler.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Arduino.h>
#include <vector>

ServoHandler::ServoHandler() 
    : pwm(Adafruit_PWMServoDriver()), 
      servoMinMax{{SERVO_MIN, SERVO_MAX}, {SERVO_MIN, SERVO_MAX}, {SERVO_MIN, SERVO_MAX}} {
    // Initialize default values
    servoPins[0] = 0;
    servoPins[1] = 1;
    servoPins[2] = 2;

    defaultServoPositions[0] = 0;
    defaultServoPositions[1] = 0;
    defaultServoPositions[2] = 0;

    for (int i = 0; i < SERVOS; i++) {
        servoPositions[i] = defaultServoPositions[i];
    }
}

void ServoHandler::setupServos() {
    pwm.begin();
    pwm.setPWMFreq(50);
    servoSetPosition(std::vector<int>(std::begin(defaultServoPositions), std::end(defaultServoPositions)));
}

std::vector<int> ServoHandler::checkParams(std::vector<int> targetPosition) {
    std::vector<int> newTargetPosition;
    for (int i = 0; i < SERVOS; i++) {
        int newPosition = servoPositions[i] + targetPosition[i];
        if (newPosition < servoMinMax[i][0]) {
            newTargetPosition.push_back(servoMinMax[i][0]);
        } else if (newPosition > servoMinMax[i][1]) {
            newTargetPosition.push_back(servoMinMax[i][1]);
        } 
        else {
            newTargetPosition.push_back(newPosition);
        }
    }
    return newTargetPosition;
}

void ServoHandler::servoMove(std::vector<int> stepVector) {
    std::vector<int> newTargetPosition = checkParams(stepVector);
    for (int i = 0; i < SERVOS; i++) {
        pwm.setPWM(servoPins[i], 0, map(newTargetPosition[i], 0, 180, SERVO_MIN, SERVO_MAX));
        servoPositions[i] = newTargetPosition[i];
    }
}

int ServoHandler::degreesToPulseWidth(int degrees) {
    return map(degrees, 0, 180, SERVO_MIN, SERVO_MAX);
}

void ServoHandler::servoSetPosition(std::vector<int> wantedPos) {
    bool allReached = false;
    std::vector<int> pulseWidthPositions(SERVOS, 0);
    std::vector<int> stepVector(SERVOS, 0);
    
    // Convert degrees to pulse width
    for (int i = 0; i < SERVOS; i++) {
        pulseWidthPositions[i] = degreesToPulseWidth(wantedPos[i]);
    }
    Serial.println("Stage7");
    
    while (!allReached) {
        allReached = true;
        
        for (int i = 0; i < SERVOS; i++) {
            if (servoPositions[i] < pulseWidthPositions[i]) {
                stepVector[i] = 1;
                allReached = false;
            } else if (servoPositions[i] > pulseWidthPositions[i]) {
                stepVector[i] = -1;
                allReached = false;
            }
            Serial.println("servoPositions");
        }
        
        
        servoMove(stepVector);
        delay(15); // Optional: Add delay to allow servos to move
    }
    Serial.println("Stage8");
}

#include "ServoHandler.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Arduino.h>
#include <vector>

ServoHandler::ServoHandler(const int defaultpos[]) : 
      servoMinMax{{SERVO_MIN, SERVO_MAX}, {SERVO_MIN, SERVO_MAX}, {SERVO_MIN, SERVO_MAX}} {
    pwm = new Adafruit_PWMServoDriver(0x40);
 
    /* Init servopins and default positions*/
    for(int i = 0; i < SERVOS; i++) {
        servoPins.push_back(i);  
        defaultServoPositions.push_back(defaultpos[i]);
    }

    for (int i = 0; i < SERVOS; i++) {
        servoPositions.push_back(defaultServoPositions[i]);
    }
}

void ServoHandler::setupServos() {
    pwm->begin();
    pwm->setPWMFreq(60);
    Serial.println("inside of setup");
    // servoSetPosition(std::vector<int>(std::begin(defaultServoPositions), std::end(defaultServoPositions)));
    // test();
    servoSetPosition(this->defaultServoPositions, "");
}

std::vector<int> ServoHandler::checkParams(std::vector<int> &targetPosition) {
    std::vector<int> newTargetPosition;
    int newPosition;

    for (int i = 0; i < SERVOS; i++) {
        newPosition = servoPositions[i] + targetPosition[i];
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

void ServoHandler::servoMove(std::vector<int> &stepVector) {
    std::vector<int> newTargetPosition = checkParams(stepVector);

    for(auto &e : stepVector) {
        Serial.println(e); 
    }
    
    for (int i = 0; i < SERVOS; i++) {
        // Move the servo one degree toward the target
        if (stepVector[i] == 1) {
            servoPositions[i] += 1;  // Increase angle by 1 degree
        } else if (stepVector[i] == -1) {
            servoPositions[i] -= 1;  // Decrease angle by 1 degree
        }

        // Ensure servoPositions[i] stays within the valid range of 0 to 180 degrees
        servoPositions[i] = constrain(servoPositions[i], 0, 180);

        // Map the new position to PWM pulse width and move the servo
        int pulseWidth = degreesToPulseWidth(servoPositions[i]);
        pwm->setPWM(servoPins[i], 0, pulseWidth);

        // // Print debug information
        // Serial.print("Servo "); 
        // Serial.print(i); 
        // Serial.print(" moved to angle: "); 
        // Serial.print(servoPositions[i]);
        // Serial.print(" -> PWM: ");
        // Serial.println(pulseWidth);
    }
}

void ServoHandler::test() {
    for(int i=0; i<8; i++)
      { pwm->setPWM(i, 0, degreesToPulseWidth(0) );}
    delay(1000);
    
    for( int angle =0; angle<181; angle +=10)
      { for(int i=0; i<8; i++)
          { pwm->setPWM(i, 0, degreesToPulseWidth(angle) );}
      }
    delay(100);    
}

int ServoHandler::degreesToPulseWidth(int degrees) {
    int pulse = map(degrees, 0, 180, SERVO_MIN, SERVO_MAX);
    Serial.print("Angle: ");Serial.print(degrees);
    Serial.print(" pulse: ");Serial.println(pulse);
    return pulse;
}

void ServoHandler::servoSetPosition(std::vector<int> &wantedPos, char debug[] = "") {
    bool allReached = false;
    std::vector<int> pulseWidthPositions(SERVOS, 0);
    std::vector<int> stepVector(SERVOS, 0);
    unsigned long currentTime = millis(); 
    
    Serial.println(debug);
    // Convert degrees to pulse width
    for (int i = 0; i < SERVOS; i++) {
        pulseWidthPositions[i] = degreesToPulseWidth(wantedPos[i]);
    }
    // Serial.print("pulswidth pos:");
    // for(auto& i: pulseWidthPositions) {
    //     Serial.print(i);    Serial.print(" "); 
    // }
    // Serial.println("");
    // Serial.println("Stage7");

    // Serial.println("Came here");
    while (!allReached) {
        allReached = true;
        
        for (int i = 0; i < SERVOS; i++) {
            if (degreesToPulseWidth(servoPositions[i]) < pulseWidthPositions[i]) {
                stepVector[i] = 1;
                allReached = false;
            } else if (degreesToPulseWidth(servoPositions[i]) > pulseWidthPositions[i]) {
                stepVector[i] = -1;
                allReached = false;
            } else {
                stepVector[i] = 0;
            }
        }
        // Serial.print("Steper values: ");
        // for(auto& element : stepVector) {
        //     Serial.print(element); Serial.print(" "); 
        // }
        Serial.println();

        // // Serial.print("Servo Positions: ");
        // // for(auto& pos : servoPositions) {
        // //     Serial.print(pos); Serial.print(" ");
        // // }
        // Serial.println();

        servoMove(stepVector); // move towards the goal 
        // // Serial.print("Servo Positions: ");
        // // for(auto& pos : servoPositions) {
        // //     Serial.print(pos); Serial.print(" ");
        // // }
        // Serial.println();

        do{
            currentTime = millis();
            // Serial.println("waiting...");
        }while(currentTime - previousTime < interval);
        previousTime = currentTime; 
    }
        

    //         // delay(15); // Optional: Add delay to allow servos to move

    Serial.println("Stage8");
}

ServoHandler::~ServoHandler() {
    delete(pwm); 
}
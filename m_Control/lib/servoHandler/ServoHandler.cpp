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

    currentVector = std::vector<int>(SERVOS, 0); // Initialize currentVector
    previousVector = std::vector<int>(SERVOS, 0); // Initialize previousVector
}

void ServoHandler::robotPickUp(){
    
    // std::vector<int> restPosition = {180, 180, 180, 90, 120};
    // servoSetPosition(restPosition, "Rotate to object position");
    // delay(500);

    std::vector<int> rotateToObject = {90, 180, 180, 90, 180};
    servoSetPosition(rotateToObject, "Rotate to object position");
    delay(500);

    std::vector<int> lowerToPick = {90, 80, 160, 180, 180};
    servoSetPosition(lowerToPick, "Rotate to object position");
    delay(500);

    std::vector<int> grabObject = {90, 80, 160, 180, 120}; 
    servoSetPosition(grabObject, "Grabbing the object");
    delay(1000);

    std::vector<int> pickUpObject = {90, 180, 180, 160, 120};
    servoSetPosition(pickUpObject, "Rotate to object position");
    delay(500);

    std::vector<int> rotateToDrope = {140, 180, 180, 90, 120};
    servoSetPosition(rotateToDrope, "Rotate to object position");
    delay(500);

    std::vector<int> lowerToDrope = {140, 80, 160, 180, 120};
    servoSetPosition(lowerToDrope, "Rotate to object position");
    delay(500);

    std::vector<int> dropTheObject = {140, 80, 160, 180, 180}; //90 for å close
    servoSetPosition(dropTheObject, "Rotate to object position");
    delay(500);

    std::vector<int> backUp = {140, 180, 180, 90, 180}; //90 for å close
    servoSetPosition(backUp, "Rotate to object position");
    delay(500);
}




void ServoHandler::setupServos() {
    pwm->begin();
    pwm->setPWMFreq(60);
    Serial.println("inside of setup");
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
void ServoHandler::servoJoints(int from, int to, const std::vector<int> &choosenServos) {
    for (int i = 0; i < choosenServos.size(); i++) {
        int servoIndex = choosenServos[i];
        std::vector<int> newPosition(SERVOS, 0);

        // Set the current positions for servos that shouldn't be moved
        for (int j = 0; j < SERVOS; j++) {
            newPosition[j] = servoPositions[j];
        }

        // Move the chosen servo from 'from' to 'to'
        newPosition[servoIndex] = from;
        servoSetPosition(newPosition, "Moving Servo");
        newPosition[servoIndex] = to;
        servoSetPosition(newPosition, "Moving Servo");
    }
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
    }
}

<<<<<<< HEAD
void ServoHandler::servoMove2(std::vector<int> &stepVector) {
=======
void ServoHandler::servoMoveModded(std::vector<int> &stepVector) {
>>>>>>> ee3e4993753f1d0593e8e82a0a65fceef2a090b1
    std::vector<int> newTargetPosition = checkParams(stepVector);

    for(auto &e : stepVector) {
        Serial.println(e); 
    }
    
    for (int i = 0; i < SERVOS; i++) {
<<<<<<< HEAD
        // Move the servo one degree toward the target
        if (stepVector[i] == 1) {
            servoPositions[i] += 4;  // Increase angle by 1 degree
        } else if (stepVector[i] == -1) {
            servoPositions[i] -= 4;  // Decrease angle by 1 degree
        }

        // Ensure servoPositions[i] stays within the valid range of 0 to 180 degrees
        servoPositions[i] = constrain(servoPositions[i], 0, 180);

        // Map the new position to PWM pulse width and move the servo
=======
        if (stepVector[i] == 1) {
            servoPositions[i] += 2;  
        } else if (stepVector[i] == -1) {
            servoPositions[i] -= 2;  
        }

        servoPositions[i] = constrain(servoPositions[i], 0, 180);

>>>>>>> ee3e4993753f1d0593e8e82a0a65fceef2a090b1
        int pulseWidth = degreesToPulseWidth(servoPositions[i]);
        pwm->setPWM(servoPins[i], 0, pulseWidth);
    }
}

<<<<<<< HEAD

void ServoHandler::servoLoop() {
    Serial.println("Inside servoLoop...");

    // Print current and previous vectors for debugging
    Serial.print("Current Vector: ");
    for (const auto& val : currentVector) {
        Serial.print(val);
        Serial.print(" ");
    }
    Serial.println();

    Serial.print("Previous Vector: ");
    for (const auto& val : previousVector) {
        Serial.print(val);
        Serial.print(" ");
    }
    Serial.println();

    if (currentVector != previousVector) {
        servoMove(currentVector);
        previousVector = currentVector;
    } else {
        servoMove(previousVector);
    }

    delay(100);
}

=======
>>>>>>> ee3e4993753f1d0593e8e82a0a65fceef2a090b1
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

void ServoHandler::servoSetPosition(std::vector<int> &wantedPos, const char* debug) {
    bool allReached = false;
    std::vector<int> pulseWidthPositions(SERVOS, 0);
    std::vector<int> stepVector(SERVOS, 0);
    unsigned long currentTime = millis(); 
    
    Serial.println(debug);
    // Convert degrees to pulse width
    for (int i = 0; i < SERVOS; i++) {
        pulseWidthPositions[i] = degreesToPulseWidth(wantedPos[i]);
    }
    Serial.print("pulswidth pos:");
    for(auto& i: pulseWidthPositions) {
        Serial.print(i);    Serial.print(" "); 
    }
    Serial.println("");
    Serial.println("Stage7");

    Serial.println("Came here");
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
        Serial.print("Steper values: ");
        for(auto& element : stepVector) {
            Serial.print(element); Serial.print(" "); 
        }
        Serial.println();

        servoMove(stepVector); // move towards the goal 

        do{
            currentTime = millis();
        }while(currentTime - previousTime < interval);
        previousTime = currentTime; 
    }
}

void ServoHandler::updateCurrentVector(const std::vector<int>& newVector) {
    currentVector = newVector;
}

ServoHandler::~ServoHandler() {
    delete(pwm); 
}
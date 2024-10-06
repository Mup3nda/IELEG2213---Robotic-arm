#ifndef SERVO_HANDLER_H
#define SERVO_HANDLER_H

#include <vector>
#include <Adafruit_PWMServoDriver.h>

class ServoHandler {
public:
    ServoHandler();
    void setupServos();
    void servoMove(std::vector<int> stepVector);
    void servoSetPosition(std::vector<int> wantedPos);
    static const int SERVO_DELAY = 1000; // Delay in milliseconds

private:
    Adafruit_PWMServoDriver pwm;
    static const int SERVOS = 3;
    static const int SERVO_MIN = 100;
    static const int SERVO_MAX = 600;

    int servoPins[SERVOS];
    const int servoMinMax[3][2];
    int defaultServoPositions[SERVOS];
    int servoPositions[SERVOS];

    std::vector<int> checkParams(std::vector<int> targetPosition);
    int degreesToPulseWidth(int degrees); // New function to convert degrees to pulse width
};

#endif // SERVO_HANDLER_H
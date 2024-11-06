#ifndef SERVO_HANDLER_H
#define SERVO_HANDLER_H

#include <vector>
#include <Adafruit_PWMServoDriver.h>

class ServoHandler {
public:
    ServoHandler(const int defaultpos[]);
    ~ServoHandler();
    void setupServos();
    void servoMove(std::vector<int> &stepVector);
    void servoMoveModded(std::vector<int> &stepVector);
    void servoSetPosition(std::vector<int> &wantedPos, char debug[]);
    static const int SERVO_DELAY = 1000; // Delay in milliseconds
    void test(); 

private:
    Adafruit_PWMServoDriver* pwm;
    static const int SERVOS = 3;
    static const int SERVO_MIN = 125; // 1ms -> 0 degree 
    static const int SERVO_MAX = 625; // 2ms -> 180 degree
    unsigned long previousTime = 0; 
    unsigned long interval = 15; 

    

    const int servoMinMax[3][2];
    std::vector<int> servoPins;
    std::vector<int> defaultServoPositions;
    std::vector<int> servoPositions;

    std::vector<int> checkParams(std::vector<int> &targetPosition);
    int degreesToPulseWidth(int degrees); // New function to convert degrees to pulse width
};

#endif // SERVO_HANDLER_H
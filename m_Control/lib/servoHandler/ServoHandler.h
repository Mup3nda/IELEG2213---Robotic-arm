#ifndef SERVO_HANDLER_H
#define SERVO_HANDLER_H

#include <vector>
#include <Adafruit_PWMServoDriver.h>

class ServoHandler {
public:
    ServoHandler(const int defaultpos[]);
    ~ServoHandler();
    void setupServos();
    void robotPickUp();
    void servoMove(std::vector<int> &stepVector);
<<<<<<< HEAD
    void servoMove2(std::vector<int> &stepVector);
    void servoSetPosition(std::vector<int> &wantedPos, const char* debug = "");
    void servoLoop();
    void updateCurrentVector(const std::vector<int>& newVector);
    void servoJoints(int from, int to, const std::vector<int> &choosenServos); // Add this line
=======
    void servoMoveModded(std::vector<int> &stepVector);
    void servoSetPosition(std::vector<int> &wantedPos, char debug[]);
>>>>>>> ee3e4993753f1d0593e8e82a0a65fceef2a090b1
    static const int SERVO_DELAY = 1000; // Delay in milliseconds
    void test(); 

private:
    Adafruit_PWMServoDriver* pwm;
<<<<<<< HEAD
    static const int SERVOS = 3;
    static const int SERVO_MIN = 100; // 0 degree 
    static const int SERVO_MAX = 660; //  180 degree
=======
    static const int SERVOS = 5; // Update to 5 servos
    static const int SERVO_MIN = 125; // 1ms -> 0 degree 
    static const int SERVO_MAX = 625; // 2ms -> 180 degree
>>>>>>> 83a8446160007dae216aadef968ed2e09104bc7a
    unsigned long previousTime = 0; 
    unsigned long interval = 20; 

    const int servoMinMax[5][2]; // Update to handle 5 servos
    std::vector<int> servoPins;
    std::vector<int> defaultServoPositions;
    std::vector<int> servoPositions;
    std::vector<int> currentVector;
    std::vector<int> previousVector;

    std::vector<int> checkParams(std::vector<int> &targetPosition);
    int degreesToPulseWidth(int degrees);
};

#endif // SERVO_HANDLER_H
#include <Wire.h>
#include "Websocket.h"
#include <ArduinoJson.h>
#include "ServoHandler.h"

/* Servo */
const int defaultPos[5] = {0, 180, 90, 180, 180};
//const int defaultPos[3] = {0, 180, 0};
ServoHandler* servoHandler = new ServoHandler(defaultPos);

/* Websocket */
const char* ssid = "ABS-Link";
const char* password = "ABS_2023";
//const char* server = "192.168.0.178"; //ABDI
const char* server = "192.168.0.218"; //DIDIER
const uint16_t port = 9000; 
void event(WStype_t type, uint8_t* payload, size_t length);  
Websocket* ws = new Websocket(ssid, password, server, port);

void setup() {
    Serial.begin(115200);
    Serial.println("Setting up...");
    servoHandler->setupServos();
    ws->begin();
    ws->setCallback(event); 
    Serial.println("Setup complete!"); 
}

void loop() {
    ws->loop(); 
  // TEST CLAWS
    std::vector<int> open = {0, 180, 90, 180, 180};
    servoHandler->servoSetPosition(open, "Rotate to object position");
    delay(500);

    std::vector<int> close = {0, 180, 90, 110, 90};
    servoHandler->servoSetPosition(close, "Rotate to object position");
    delay(500);

            // TEST CLAWS

    std::vector<int> close = {180, 180, 90, 90, 90};
    servoHandler->servoSetPosition(close, "Rotate to object position");
    delay(500);
    Serial.println("\n\n270\n\n");
    std::vector<int> open2 = {180, 180, 90, 180, 180};
    servoHandler->servoSetPosition(open2, "Rotate to object position");
    delay(1000);
    Serial.println("\n\nREST\n\n");

            // TEST CLAWS
    std::vector<int> open3 = {180, 180, 90, 180, 90};
    servoHandler->servoSetPosition(open3, "Rotate to object position");
    delay(1000);
    Serial.println("\n\n90\n\n");

}

void event(WStype_t type, uint8_t* payload, size_t length) {
// Ensure all vectors are properly initialized
    std::vector<int> Orientation = {0, 0, 0, 0, 90}; 
    std::vector<int> home = {defaultPos[0], defaultPos[1], defaultPos[2], defaultPos[3], 180}; 
    std::vector<int> dropGoal = {0, 130, 70, 120, 90}; 
    // std::vector<int> dropGoal = {0, 90, 130, 90, 90}; 


    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("Disconnected!");
            break;
        case WStype_CONNECTED:
            Serial.println("Connected to WebSocket server");
            break;
        case WStype_TEXT: {
            Serial.print("Received message: ");
            Serial.println((char*)payload);
            const char* json = (char*)payload; 
            StaticJsonDocument<200> doc; 

            DeserializationError error = deserializeJson(doc, json); 
            if(error) {
                Serial.print(F("deserializeJson() failed: "));
                Serial.println(error.c_str());
                return;
            }
            
            if(json[0] != '"') {
                Serial.print("Received Allowed message:");
                JsonArray angles = doc.as<JsonArray>(); 
                Serial.println((char*)payload);
                for(int i = 0; i < 4; i++) {
                    Orientation[i] = angles[i]; 
                }
                // Ensure the gripper is open
                Orientation[4] = 180;
                Serial.print("Wanted gripper angle: ");
                Serial.println(Orientation[4]);
                servoHandler->servoSetPosition(Orientation, "Moving to goal");
                delay(1000);
                Serial.print("Current Orientation: ");
                for (auto value : Orientation) {
                    Serial.print(value);
                    Serial.print(" ");
                }
                Serial.println();

                // Close the gripper to grip the object
                delay(1000);
                Orientation[4] = 90;
                servoHandler->servoSetPosition(Orientation, "Gripping object");
                delay(1000);

                // Move to home position
                home[4] = 90; // Ensure gripper stays closed
                servoHandler->servoSetPosition(home, "Returning to home position");
                delay(1000);

                // Move to drop position
                dropGoal[4] = 90;
                servoHandler->servoSetPosition(dropGoal, "Moving to drop position");
                delay(1000);

                // Open the gripper to drop the object
                dropGoal[4] = 180;
                servoHandler->servoSetPosition(dropGoal, "Dropping object");
                delay(1000);

                // Return to home position
                home[4] = 180;
                Serial.println("Returning to home position...");
                servoHandler->servoSetPosition(home, "Returning to home position");
                delay(1000);
            }
            break;
        }
        case WStype_BIN:
            Serial.println("Received binary data");
            break;
    }
}

    // Serial.println("\n\n\n START \n\n\n");
    // servoHandler->robotPickUp();

    // // TEST CLAWS
    // std::vector<int> open = {180, 180, 90, 90, 90};
    // servoHandler->servoSetPosition(open, "Rotate to object position");
    // delay(1000);
    // Serial.println("\n\nCounter Clockwise\n\n");

    // std::vector<int> close = {180, 180, 90, 190, 95};
    // servoHandler->servoSetPosition(close, "Rotate to object position");
    // delay(1000);
    // Serial.println("\n\nClockwise\n\n");

    // std::vector<int> stop = {180, 180, 90, 180, 90};
    // servoHandler->servoSetPosition(stop, "Rotate to object position");
    // delay(1000);
    // Serial.println("\n\nCounter Clockwise\n\n");

    // // TEST CLAWS
    // std::vector<int> back = {180, 180, 90, 10, 85};
    // servoHandler->servoSetPosition(back, "Rotate to object position");
    // delay(1000);
    // Serial.println("\n\nBack\n\n");

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
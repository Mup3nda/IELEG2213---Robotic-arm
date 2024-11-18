#include <Wire.h>
#include <Websocket.h>
#include <ArduinoJson.h>
#include "ServoHandler.h"

/* Servo */
const int defaultPos[5] = {0, 180, 90, 180, 180};
ServoHandler* servoHandler = new ServoHandler(defaultPos);

/* Websocket */
const char* ssid = "ABS-Link";
const char* password = "ABS_2023";
const char* server = "192.168.0.178";
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
//   // TEST CLAWS
//     std::vector<int> open = {0, 180, 90, 180, 180};
//     servoHandler->servoSetPosition(open, "Rotate to object position");
//     delay(500);

//     std::vector<int> close = {0, 180, 90, 110, 90};
//     servoHandler->servoSetPosition(close, "Rotate to object position");
//     delay(500);
}

void event(WStype_t type, uint8_t* payload, size_t length) {
    std::vector<int> Orientation = {0, 0, 0, 0, 90}; 
    std::vector<int> home = {defaultPos[0], defaultPos[1], defaultPos[2], 90};
     std::vector<int> currentPostions; 

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
                for(auto &pos : servoHandler->getServoPostions()) {
                    currentPostions.push_back(pos); 
                }

                if(Orientation[4] == currentPostions[4]) { // if its gripping something 
                    servoHandler->servoSetPosition(home, "going towards home"); 
                    servoHandler->servoSetPosition(Orientation, "Moving towards the drop point");
                    delay(500); 
                    Orientation[4] = 180; 
                    servoHandler->servoSetPosition(Orientation, "Dropping");
                    delay(500); 
                    home[4] = defaultPos[4]; 
                    servoHandler->servoSetPosition(home, "back to home"); 
                } else {
                    servoHandler->servoSetPosition(Orientation, "Moving towards goal"); 
                    servoHandler->updateCurrentVector(Orientation); 
                }
                // delay(500);
                // Orientation[4] = 90; 
                // servoHandler->servoSetPosition(Orientation, "Closing");
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
    // std::vector<int> open = {180, 180, 180, 90, 180};
    // servoHandler->servoSetPosition(open, "Rotate to object position");
    // delay(500);

    // std::vector<int> close = {180, 180, 180, 90, 90};
    // servoHandler->servoSetPosition(close, "Rotate to object position");
    // delay(500);



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
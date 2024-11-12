#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "ServoHandler.h"
#include <Websocket.h>
#include <ArduinoJson.h>

/* Kinematics */
const int defaultPos[3] = {0, 180, 0};
// std::vector<int> pos = {180, 180, 180};

/* Websocket */
const char* ssid = "ABS-Link";
const char* password = "ABS_2023";
const char* server = "192.168.0.178";
const uint16_t port = 9000;
void event(WStype_t type, uint8_t* payload, size_t length); 


ServoHandler* servoHandler = new ServoHandler(defaultPos);
Websocket* ws = new Websocket(ssid, password, server, port);

void setup() {
    Serial.begin(115200);
    Serial.println("Alternate Servo Test");
    servoHandler->setupServos();
    ws->begin();
    ws->setCallback(event);
}

void loop() {
    ws->loop();

    // servoHandler->servoSetPosition(pos, "To position");
    // Serial.println("Break...");
    // delay(5000);
}


void event(WStype_t type, uint8_t* payload, size_t length) {
    std::vector<int> Orientation = {0, 0, 0}; 

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

            JsonArray angles = doc.as<JsonArray>(); 
            for(int i = 0; i < 3; i++) {
                Orientation[i] = angles[i]; 
            }
            servoHandler->servoSetPosition(Orientation, ""); 
            break;
        }
        case WStype_BIN:
            Serial.println("Received binary data");
            break;
    }
}


/** 
*   General info: 
*   -------------
* - Arm 1 i 90 angle = 110 angle    
* - Arm 2 i 90 angle = 50 angle  
*/
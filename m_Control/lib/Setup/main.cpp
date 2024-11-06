#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "ServoHandler.h"  

using namespace websockets;

const char* ssid = "ABS-Link";
const char* password = "ABS_2023";
WebsocketsServer server;
const int defaultPos[5] = {180, 180, 180, 180, 180};

ServoHandler* servoHandler;

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi!");
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
}

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    server.listen(81);
    Serial.print("WebSocket server started at ws://");
    Serial.print(WiFi.localIP());
    Serial.println(":81");

    // Initialize the ServoHandler instance
    servoHandler = new ServoHandler(defaultPos);
    servoHandler->setupServos();
}

void loop() {
    WebsocketsClient client = server.accept();
    if (client.available()) {
        Serial.println("Client connected to WebSocket server");

        while (client.available()) {
            client.poll();  // Poll for messages
            WebsocketsMessage message = client.readBlocking();  // Read incoming message

            if (message.isEmpty()) {
                continue;
            }

            Serial.print("Received message: ");
            Serial.println(message.data());



            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, message.data());
            if (error) {
                Serial.print("JSON deserialization failed: ");
                Serial.println(error.c_str());
                continue;
            }

            if (doc.is<JsonArray>()) {
                Serial.print("Received vector: ");
                std::vector<int> stepVector;

                for (JsonVariant v : doc.as<JsonArray>()) {
                    Serial.print(v.as<int>());
                    Serial.print(" ");
                    stepVector.push_back(v.as<int>());
                }

                Serial.println();
                servoHandler->servoMoveModded(stepVector);
            } else {
                Serial.println("Received message is not a vector");
            }
        }
        Serial.println("Client disconnected");
    }
}

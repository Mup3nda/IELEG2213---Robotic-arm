#ifndef WEBSOCKET_H
#define WEBSOCKET_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <Wire.h>

class Websocket {
    private: 
        const char* ssid;
        const char * password; 
        const char* server; 
        const uint16_t port;

        WebSocketsClient* ws; 

    public:
        Websocket(const char* ssid, const char* pass, const char* server, const uint16_t port);
        ~Websocket();
        void begin(); 
        void EventHandler(WStype_t type, uint8_t * payload, size_t length);   
        void loop(); 
}; 

#endif WEBSOCKET_H
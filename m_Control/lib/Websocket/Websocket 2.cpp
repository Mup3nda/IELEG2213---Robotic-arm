#include "Websocket.h"

/** 
*   @param ssid[] => Network name
*   @param pass[] => wifi password
*   @param server[] => server name
*   @param port => port number  
*/
Websocket::Websocket(const char* ssid, const char* pass, const char* server, const uint16_t port) 
: ssid(ssid), password(pass), server(server), port(port) {
    ws = new WebSocketsClient; 
}

Websocket::~Websocket() {
    delete(ws); 
}

void Websocket::begin() {
    WiFi.begin(ssid, password); 
    while(WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    ws->begin(server, port); 
    ws->onEvent([this](WStype_t type, uint8_t * payload, size_t length) {
        this->EventHandler(type, payload, length);
    });
}

void Websocket::EventHandler(WStype_t type, uint8_t * payload, size_t length) {
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
            break;
        }
        case WStype_BIN:
            Serial.println("Received binary data");
            break;
    } 
}

void Websocket::loop() {
    ws->loop();
}
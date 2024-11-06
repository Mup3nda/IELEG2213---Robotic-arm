// // #include <NimBLEDevice.h>

// // const int LED_PIN_D2 = D2;  // GPIO pin connected to the LED D2
// // const int LED_PIN_D3 = D3;  // GPIO pin connected to the LED D3
// // const int LED_PIN_D4 = D4;  // GPIO pin connected to the LED D4
// // const int LED_PIN_D5 = D5;  // GPIO pin connected to the LED D5

// // NimBLECharacteristic *pCharacteristic;

// // class MyCallbacks: public NimBLECharacteristicCallbacks {
// //     void onWrite(NimBLECharacteristic* pCharacteristic) {
// //         std::string rxValue = pCharacteristic->getValue();
        
// //         // Print the received value to the serial monitor
// //         Serial.print("Received value: ");
// //         Serial.println(rxValue.c_str());

// //         if (rxValue == "D2_toggle") {
// //             digitalWrite(LED_PIN_D2, !digitalRead(LED_PIN_D2));  // Toggle LED D2
// //             Serial.println("LED D2 toggled");
// //         } else if (rxValue == "D3_toggle") {
// //             digitalWrite(LED_PIN_D3, !digitalRead(LED_PIN_D3));  // Toggle LED D3
// //             Serial.println("LED D3 toggled");
// //         } else if (rxValue == "D4_toggle") {
// //             digitalWrite(LED_PIN_D4, !digitalRead(LED_PIN_D4));  // Toggle LED D4
// //             Serial.println("LED D4 toggled");
// //         } else if (rxValue == "D5_toggle") {
// //             digitalWrite(LED_PIN_D5, !digitalRead(LED_PIN_D5));  // Toggle LED D5
// //             Serial.println("LED D5 toggled");
// //         }
// //     }
// // };

// void setup() {
//   Serial.begin(115200);
// //   pinMode(LED_PIN_D2, OUTPUT);  // Set LED pin D2 as output
// //   pinMode(LED_PIN_D3, OUTPUT);  // Set LED pin D3 as output
// //   pinMode(LED_PIN_D4, OUTPUT);  // Set LED pin D4 as output
// //   pinMode(LED_PIN_D5, OUTPUT);  // Set LED pin D5 as output

// //   NimBLEDevice::init("ESP32_LED_Control");

// //   NimBLEServer *pServer = NimBLEDevice::createServer();
// //   NimBLEService *pService = pServer->createService("12345678-1234-1234-1234-123456789abc");

// //   pCharacteristic = pService->createCharacteristic(
// //                       "87654321-4321-4321-4321-abc123456789",
// //                       NIMBLE_PROPERTY::WRITE
// //                     );
  
// //   pCharacteristic->setCallbacks(new MyCallbacks());

// //   pService->start();

// //   NimBLEAdvertising *pAdvertising = NimBLEDevice::getAdvertising();
// //   pAdvertising->addServiceUUID("12345678-1234-1234-1234-123456789abc");
// //   pAdvertising->start();

// //   Serial.println("Waiting for a BLE client to connect...");
// }

// void loop() {
//   // Nothing to do here, everything is handled in the callback
// }

#include <Websocket.h>

// Replace with your network credentials
const char* ssid = "ABS-Link";
const char* password = "ABS_2023";

// WebSocket server details
const char* server = "192.168.0.178";
const uint16_t port = 9000; // Replace with your server port

Websocket* ws = new Websocket(ssid, password, server, port);  

void setup() {
    Serial.begin(115200);
    ws->begin();
}

void loop() {
    // Keep the connection alive
    ws->loop();

    // unsigned long currentMillis = millis();
    // if (currentMillis - previousMillis >= interval) {
    //     previousMillis = currentMillis;
    //     Serial.println("Sending message to server...");
    //     webSocket.sendTXT("Hello from Arduino!");
    // }
}
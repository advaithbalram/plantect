#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

#define DHTPIN 4     // Digital pin the DHT11 is connected to
#define DHTTYPE DHT11   // Type of DHT sensor

DHT dht(DHTPIN, DHTTYPE);
const char *ssid = "********";     // Replace the * with your WiFi SSID
const char *password = "*******";       // Replace the * with your WiFi password
const char *server_url = "https://plantect-backend.onrender.com/api/sensor"; // Your backend hosted URL and path

WiFiClientSecure client;  // Use WiFiClientSecure instead of WiFiClient
HTTPClient http;    // Declare the HTTPClient object

void setup() {
   delay(3000);
   Serial.begin(9600);
   dht.begin();
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.print(".");
   }
   Serial.println("WiFi connected");
   client.setInsecure();  // This will allow all SSL certificates.
   delay(1000);
}

void loop() {
   float h = dht.readHumidity();
   float t = dht.readTemperature();         
   Serial.print("Humidity = ");
   Serial.print(h);
   Serial.print("%  ");
   Serial.print("Temperature = ");
   Serial.print(t); 
   Serial.println("C  ");
   
   StaticJsonDocument<200> jsonBuffer; // Create JSON buffer
   JsonObject values = jsonBuffer.to<JsonObject>();
   values["humidity"] = h;
   values["temperature"] = t;

   // Serialize JSON object to String
   String jsonStr;
   serializeJson(values, jsonStr);

   // Send POST request to server
   if (http.begin(client, server_url)) {
       http.setTimeout(15000);
       http.addHeader("Content-Type", "application/json");
       int httpCode = http.POST(jsonStr);
       if (httpCode > 0) {
           if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
               String payload = http.getString();
               Serial.print("Response: ");
               Serial.println(payload);
           } else if (httpCode == HTTP_CODE_TEMPORARY_REDIRECT) {
               String newLocation = http.header("Location");
               Serial.printf("[HTTP] Redirecting to: %s\n", newLocation.c_str());
               http.end();

               if (http.begin(client, newLocation)) {
                   http.addHeader("Content-Type", "application/json");
                   httpCode = http.POST(jsonStr);
                   if (httpCode > 0) {
                       if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
                           String payload = http.getString();
                           Serial.print("Response: ");
                           Serial.println(payload);
                       } else {
                           Serial.printf("[HTTP] POST to new location... failed, status code: %d\n", httpCode);
                           Serial.println("Response payload: " + http.getString());
                       }
                   } else {
                       Serial.printf("[HTTP] POST to new location... failed, error: %s\n", http.errorToString(httpCode).c_str());
                   }
                   http.end();
               } else {
                   Serial.println("Unable to connect to new location");
               }
           } else {
               Serial.printf("[HTTP] POST... failed, status code: %d\n", httpCode);
               Serial.println("Response payload: " + http.getString());
           }
       } else {
           Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
       }
       http.end();
   } else {
       Serial.println("Unable to connect to server");
   }
   
   delay(5000); // Delay before next reading
}
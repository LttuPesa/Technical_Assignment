#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* ssid = "vira";
const char* password = "vira1234";

const char* serverAddress = "http://192.168.100.4:5000/submit-data"; // server saya

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float temperature = dht.readTemperature();
  if (isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }
  
  HTTPClient http;
  http.begin(serverAddress);
  http.addHeader("Content-Type", "application/json");
  
  String jsonData = "{\"temperature\":" + String(temperature) + "}";
  
  int httpResponseCode = http.POST(jsonData);
  
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
  
  delay(10000);
}

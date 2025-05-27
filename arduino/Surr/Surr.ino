#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// Replace with your WiFi credentials
const char* ssid = "Scythe-20";
const char* password = "3a1b4c1d";

// Firebase Realtime Database URL
const String firebaseHost = "https://ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app"; // include trailing slash

// If using database secret token (Deprecated for production, OK for test)
const String firebaseAuth = "HZbsP9VskKkdZicGIbhFx7PJXvv8YFBJSOQXsx2t";

// Firebase node to push data
const String firebasePath = "/sensorData.json"; // .json is required for REST API

// Pins
#define DHTPIN 5
#define DHTTYPE DHT22
#define PIR_PIN 14
#define BUZZER_PIN 25
#define MQ2_PIN 34

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  dht.begin();
  
  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");
  
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int motion = digitalRead(PIR_PIN);
  int gas = analogRead(MQ2_PIN);

  if (!isnan(temp) && !isnan(hum)) {
    String jsonPayload = "{\"temperature\":" + String(temp) + 
                         ",\"humidity\":" + String(hum) + 
                         ",\"motion\":" + String(motion) + 
                         ",\"gas\":" + String(gas) + "}";

    Serial.print(jsonPayload);
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      String fullURL = firebaseHost + firebasePath + "?auth=" + firebaseAuth;

      http.begin(fullURL);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.PUT(jsonPayload); // or .POST() if pushing to a list

      Serial.print("📡 Firebase response: ");
      Serial.println(httpResponseCode);
      http.end();
    }
  } else {
    Serial.println("⚠️ Failed to read from DHT sensor!");
  }

  // Optional: alert logic
  if (motion) {
    digitalWrite(BUZZER_PIN, HIGH);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  delay(1000); // Wait before next reading
}

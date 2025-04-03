#include <DHT.h>

// Motion Sensor & DHT22
#define PIR_PIN 13
#define LED_PIN 4
#define DHT_PIN 5
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(115200); // Start Serial communication

    pinMode(PIR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    
    Serial.println("ESP32 Sensor Data Logger Initialized...");
    dht.begin();
}

void loop() {
    int motion = digitalRead(PIR_PIN);
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Failed to read from DHT22 sensor!");
    } else {
        // Send data over Serial
        Serial.print("T:");
        Serial.print(temperature);
        Serial.print(",H:");
        Serial.print(humidity);
        Serial.print(",M:");
        Serial.println(motion);
    }

    if (motion == HIGH) {
        digitalWrite(LED_PIN, HIGH);
        Serial.println("Motion Detected!");
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    delay(2000); // Send data every 2 seconds
}
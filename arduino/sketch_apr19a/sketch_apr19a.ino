#include <WiFi.h>
#include <Firebase_ESP_Client.h>  // ✅ This is correct


// Wi-Fi credentials
#define WIFI_SSID "Scythe-20"
#define WIFI_PASSWORD "3a1b4c1d"

// Firebase credentials
#define API_KEY "AIzaSyAVmVJ3Fp3KlplcUkX5mYnkpBTsZWhu2r4"  // Replace with your Web API Key from Firebase Console
#define DATABASE_URL "ard-cloud-test-default-rtdb.asia-southeast1.firebasedatabase.app"

// Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\n✅ Wi-Fi Connected");

  // Firebase config
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  // Optional: Use anonymous auth
  auth.user.email = "a@gmail.com";
  auth.user.password = "aaaaaaaaa";

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Push "hello world" to the database
  if (Firebase.RTDB.setString(&fbdo, "/test/message", "hello world")) {
    Serial.println("✅ Sent to Firebase!");
  } else {
    Serial.print("❌ Firebase Error: ");
    Serial.println(fbdo.errorReason());
  }
}

void loop() {
  // Nothing here
}
#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <HTTPClient.h>

const char* ssid = "wifi_19-310";
const char* password = "wifi19310";

WebServer server(80);
String serverIP = "";

const int led = LED_BUILTIN;
const int sensorPin = 34;


void sendSensorData() {
  HTTPClient http;
  int sensorValue = analogRead(sensorPin);  // 센서 값 읽기
  http.begin("http://" + serverIP + ":8000/pots/control_sensorData/");  // Django URL
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");  // POST 요청 시 헤더 설정

  // POST 요청으로 센서 값 전송
  String postData = "sensor_value=" + String(sensorValue);
  int httpCode = http.POST(postData);

  if (httpCode > 0) {
    Serial.printf("[HTTP] POST... code: %d\n", httpCode);
  } else {
    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();
}


void handlePump() {
  Serial.println("Activating pump...");
  digitalWrite(12, HIGH);
  digitalWrite(13, LOW);
  delay(10000);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  server.send(200, "text/plain", "Pump activated");
  Serial.println("Pump activated.");
}


void handleNotFound() {
  digitalWrite(led, LOW);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, HIGH);
}


void setup(void) {
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  delay(1000);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // 서버 IP 입력 요청
  Serial.println("Enter server IP: ");
  while (Serial.available() == 0) {}  // 입력 대기
  serverIP = Serial.readString();  // IP 주소 읽기
  
  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }
  digitalWrite(led, HIGH);

  server.on("/pump", handlePump);

  server.begin();
  Serial.println("HTTP server started");
}


void loop(void) {
  server.handleClient();
  sendSensorData();
  delay(5000);
}
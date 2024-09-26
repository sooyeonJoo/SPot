#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <HTTPClient.h>

const char* ssid = "JIUS22+WB";
const char* password = "19940322";

WebServer server(80);

const int led = LED_BUILTIN;
const int sensorPin = 34;

bool request = false;


void restRequest() {
  
  HTTPClient http;
  http.begin("http://192.168.0.13:8000/crawler_api");  //HTTPS example connection
  //http.begin("http://www.arduino.php5.sk/rele/rele1.txt"); //HTTP example connection
  //if uncomment HTTP example, you can comment root CA certificate too!
  int httpCode = http.GET();
  if (httpCode > 0) {
    Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    //file found at server --> on unsucessful connection code will be -1
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
      // server.send(200, "text/plain", payload);
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    server.send(404, "text/plain", server.arg(0) + " is not responding.");

  }
  http.end();
}

void handleRoot() {
  digitalWrite(led, LOW);
  server.send(200, "text/plain", "hello from esp32!");
  delay(1000);          // led on 유지
  digitalWrite(led, HIGH);
}

void handleURI() {
  digitalWrite(led, LOW);

  if (server.args() > 0) {
    for (int i = 0 ; i < server.args() ; i++) {
      Serial.print(server.argName(i));
      Serial.print("  ");
      Serial.println(server.arg(i));
    }
    restRequest();      // http responsd 처리
  }
  digitalWrite(led, HIGH);

}

void sendSensorData() {
  HTTPClient http;
  int sensorValue = analogRead(sensorPin);  // 센서 값 읽기
  http.begin("http://192.168.100.231:8000/pots/control_sensorData/");  // Django URL
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
  digitalWrite(led, LOW);
  digitalWrite(12, HIGH);
  digitalWrite(13, LOW);
  delay(1000);
  server.send(200, "text/plain", "Pump activated");
  digitalWrite(12, LOW);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  digitalWrite(led, HIGH);
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

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }
  digitalWrite(led, HIGH);

  server.on("/", handleRoot);
  server.on("/client", handleURI);
  server.on("/pump", handlePump);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  request = false;

  server.handleClient();

  sendSensorData();
  delay(5000);
}
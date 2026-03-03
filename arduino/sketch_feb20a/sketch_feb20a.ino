#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define DEVICE_NAME "ARD1"

Adafruit_BME280 bme_inside;
Adafruit_BME280 bme_outside;

bool inside_ok = false;
bool outside_ok = false;

void setup() {
  Serial.begin(9600);
  delay(2000);  // Allow serial to stabilize

  // Initialize INSIDE BME (0x76)
  inside_ok = bme_inside.begin(0x76);
  if (!inside_ok) {
    Serial.println("ERROR,INSIDE,BME280_NOT_FOUND");
  }

  // Initialize OUTSIDE BME (0x77)
  outside_ok = bme_outside.begin(0x77);
  if (!outside_ok) {
    Serial.println("ERROR,OUTSIDE,BME280_NOT_FOUND");
  }
}

void sendBMEReading(const char* sensorName, Adafruit_BME280 &bme) {
  float temp = bme.readTemperature();
  float hum  = bme.readHumidity();
  float pres = bme.readPressure() / 100.0F;

  Serial.print(DEVICE_NAME);
  Serial.print(",");
  Serial.print(sensorName);
  Serial.print(",BME280,");
  Serial.print(temp, 2);
  Serial.print(",");
  Serial.print(hum, 2);
  Serial.print(",");
  Serial.println(pres, 2);
}

void loop() {

  if (inside_ok) {
    sendBMEReading("INSIDE", bme_inside);
  }

  if (outside_ok) {
    sendBMEReading("OUTSIDE", bme_outside);
  }

  delay(3000);  // 3 seconds between readings
}

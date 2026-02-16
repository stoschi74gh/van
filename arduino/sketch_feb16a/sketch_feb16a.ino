#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

void setup() {
  Serial.begin(9600);
  delay(1000);

  //Serial.println("BME280 test");

  if (!bme.begin(0x76)) {
    //Serial.println("Could not find BME280 sensor!");
    while (1);
  }

  //Serial.println("BME280 found!");
}

void loop() {
  float temp = bme.readTemperature();
  float hum  = bme.readHumidity();
  float pres = bme.readPressure() / 100.0F;

  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(pres);

  delay(2000);
}

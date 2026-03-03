#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  delay(1000);

  //Serial.println("Scanning BME280");

  if (!bme.begin(0x76)) {
    //Serial.println("Could not find BME280 sensor!");
    while (1);
  }

  //Serial.println("BME280 found!");
}

void loop() {
  float temp = bme.readTemperature();
  float hum  = bme.readHumidity();
  float pres = bme.readPressure()/101325; // conversion hpa to atm

  Serial.print("Arduino1");
  Serial.print(",");
  Serial.print("Inside");
  Serial.print(",");
  Serial.print("BME280");
  Serial.print(",");
  //Serial.print("T:");
  Serial.print(temp);
  Serial.print(",");
  //Serial.print("H:");
  Serial.print(hum);
  Serial.print(",");
  //Serial.print("P:");
  Serial.println(pres);

  delay(5000);
}

#include "header.h"

void setup()
{
  Serial.begin(115200);
  Serial.print("Enter serverName: ");
  while (!Serial.available());
  serverName = Serial.readString();
  Serial.println("You entered: " + serverName);
  connectWiFi();
  i2sInit();
  xTaskCreate(micTask, "micTask", 10000, NULL, 1, NULL);
}

void loop()
{
}

#include "camera_web_server.h"
void serialInit()
{
  Serial.begin(115200);
  Serial.setDebugOutput(true);
}

void setup()
{
  Serial.begin(115200);
  Serial.print("Enter serverName: ");
  while (!Serial.available());
  serverName = Serial.readString();
  Serial.println("You entered: " + serverName);

  serialInit();
  webServerInit();
}

void loop()
{
  webServerLoop();
}

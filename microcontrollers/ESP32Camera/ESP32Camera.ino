#include "camera_web_server.h"

void serialInit() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
}

void setup() {
  serialInit();
  // bleInit();
  webServerInit();
}

void loop() {
  webServerLoop();
}


#include "header.h"

void setup()
{
  Serial.begin(115200);
  Serial.print("Enter serverName: ");
  while (!Serial.available());
  serverName = Serial.readString();
  Serial.println("You entered: " + serverName);
  connectWiFi(ssid, password);
  i2sInit();
  xTaskCreate(micTask, "micTask", 10000, NULL, 1, NULL);
  xTaskCreate(servoTask, "servoTask", 1024, NULL, 1, NULL);
}

void split(String src, String *&out, char delimiter = ' ', int max_len = 2)
{
  out = new String[max_len];
  int id = 0;
  String current = "";
  for (char c : src)
  {
    if (c != delimiter)
      current += c;
    else
    {
      if (id < max_len)
        out[id] = current.c_str();
      current = "";
      id++;
    }
    if (id >= max_len)
      return;
  }

  if (current.length() > 0 && id < max_len)
    out[id] = current.c_str();
}

void loop()
{
  if (Serial.available())
  {
    String wifi = Serial.readString();
    String *wifiData = NULL;
    wifi.trim();
    split(wifi.c_str(), wifiData, '|');
    if (wifiData == NULL)
    {
      Serial.println("what");
    }
    connectWiFi(wifiData[0].c_str(), wifiData[1].c_str());
  }
}

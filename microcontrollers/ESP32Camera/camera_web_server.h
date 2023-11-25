#pragma once
#include <Vector.h>

#ifndef CAMERA_WEB_SERVER_H
#define CAMERA_WEB_SERVER_H

#define DEFAULT_SSID "BEAN HONG COFFEE - 2.4Ghz"
#define DEFAULT_PASSWORD "11119999"
extern String serverName;
void connectWifi(String ssid, String password);
Vector<String> split(String src, char delimiter);
void webServerInit();
void webServerLoop();

#endif
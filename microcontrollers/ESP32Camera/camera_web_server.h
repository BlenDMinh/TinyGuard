#include<Vector.h>
// ===========================
// Enter your WiFi credentials
// ===========================
#define DEFAULT_SSID "ANH MINH"
#define DEFAULT_PASSWORD "ComTMM0112"

void startCameraServer();
void connectWifi(String ssid, String password);
Vector<String> split(String src, char delimiter);
void webServerInit();
void webServerLoop();
#include <Vector.h>
// ===========================
// Enter your WiFi credentials
// ===========================
#define DEFAULT_SSID "BEAN HONG COFFEE - 2.4Ghz"
#define DEFAULT_PASSWORD "11119999"

void startCameraServer();
void connectWifi(String ssid, String password);
Vector<String> split(String src, char delimiter);
void webServerInit();
void webServerLoop();
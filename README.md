[![PyTorch](https://img.shields.io/badge/PyTorch-red?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-blue?logo=flask)](https://flask.palletsprojects.com/en/3.0.x/)
[![Arduino](https://img.shields.io/badge/Arduino-green?logo=arduino)](https://www.arduino.cc/)
[![ESP32](https://img.shields.io/badge/ESP32-grey)]([https://flutter.dev/](https://www.espressif.com/en/products/socs/esp32))
[![Flutter](https://img.shields.io/badge/Flutter-blue?logo=flutter)](https://flutter.dev/)
[![Dart](https://img.shields.io/badge/Dart-blue?logo=dart)](https://dart.dev/)
[![Last Commit](https://img.shields.io/github/last-commit/BlenDMinh/TinyGuard?style=flat-square)](https://github.com/BlenDMinh/TinyGuard/commits/main)
<div align="center">
    <h1>TinyGuard</h1>
    <h3>Baby crying detection system</h3>
    <h3>A project made for Danang University's learning subject</h3>
</div>

## Project Overview 🧐

TinyGuard is an application which provides the parental control with automation for the baby caretakers. TinyGuard systems enable the ability for the parents to watch over and take care of the baby from afar with ease with the support of the lastest Artifical Intelligence technology.

### Main Features: 👌

1. **Baby Crying Detection:** Detect wether your baby is crying or not, raise alarm to notify the parents if the baby is crying.
2. **Automatically Swing:** Automatically swing the baby's crib if the baby is crying, attemp to comfort the baby.
3. **Surveillance Camera:** Monitoring your baby from afar from the mobile application.

## Client Application Demo
<div align='center'>
    <img src='https://github.com/user-attachments/assets/89244574-e852-4dd0-bfc3-cc0d65fe10bf' width=250 />
    <img src='https://github.com/user-attachments/assets/deff67ad-3ee2-4912-adcd-a6694c1bf7df' width=250 />
    <img src='https://github.com/user-attachments/assets/247213ab-df06-499e-b686-83ad450e54e1' width=250 />
</div>
<div align='center'>
    <img src='https://github.com/user-attachments/assets/24098783-57f8-4807-87f1-99c6353ae5fe' height=250 />
</div>



## Project System

![Project System](https://i.imgur.com/5kqL6VO.png)

## Getting Started
### 1. AI Server
Everything of the server is located inside **/server** folder
```
cd server
```
Install prerequisites
```
pip install -r requirements.txt
```
Server configurations can be edited inside **config.py** file. By default server is hosted on port 5000

Run the server
```
py main.py
```
### 2. Microcontrollers
Everything of the microcontrollers is located inside **/microcontrollers** folder

For this part, you need 2 Arduino boards: **ESP32-CAM** and **ESP32 DEVKIT**, a microphone module, in this system we are using **I2S INMP441**, a servo module for the crib swinging automation.

- **ESP32-CAM** will only capture and send image to the server for the image prediction.
- **ESP32 DEVKIT** will record the audio and send to the server for the audio prediction, it will also receive the prediction result from the server and swing the crib according to the result.

The schema of the microcontrollers can be seen and adjusted in the code.

Open **Arduino IDE** and upload the project code: 
- **ESP32Camera** to **ESP32-CAM**
- **ESP32Audio** to **ESP32 DEVKIT**

### 3. Client App
Everything of the client app is located inside **/client** folder
```
cd client
```
Install prerequisites
```
flutter pub get
```
You can either run the application in emulator by:
```
flutter run lib/main.dart
```
or build the **.apk** file for production:
```
flutter build apk
```

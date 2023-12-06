import 'dart:async';
import 'dart:io';
import 'dart:ui';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/services.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:intl/intl.dart';
import 'package:tinyguard/data/repository/device_repository.dart';
import 'package:tinyguard/service/alarm_player.dart';

@pragma("vm:entry-point")
class DeviceBackgroundService {
  static final FlutterBackgroundService service = FlutterBackgroundService();

  static final AndroidNotificationChannel channel = AndroidNotificationChannel(
    'tinyguard_foreground_service', // id
    'TinyGuard Foreground Service', // title
    description:
        'This channel is used for important notifications.', // description
    importance: Importance.high, // importance must be at low or higher level
  );

  static final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  static final List<Device> _devices = [];
  static final List<StreamSubscription> _streams = [];

  static int last = 0;
  static bool isCameraCrying = false;
  static bool isMicroCrying = false;
  static const int interval = 10000;

  static void addDevice(Device device) {
    _devices.add(device);
    _streams.add(device.image_predicts.stream.listen((predict) {
      if (isCameraCrying &&
          DateTime.now().millisecondsSinceEpoch - last >= interval) {
        isCameraCrying = false;
      }
      if (predict.is_crying && !isCameraCrying) {
        last = DateTime.now().millisecondsSinceEpoch;
        isCameraCrying = true;
        service.invoke(
          "onCameraBabyCrying",
          {"id": device.code},
        );
      } else if (!predict.is_crying && isCameraCrying) {
        isCameraCrying = false;
      }
    }));

    _streams.add(device.audio_streams.stream.listen((predict) {
      if (isMicroCrying &&
          DateTime.now().millisecondsSinceEpoch - last >= interval) {
        isMicroCrying = false;
      }
      if (predict.prediction == "Cry" && !isMicroCrying) {
        last = DateTime.now().millisecondsSinceEpoch;
        isMicroCrying = true;
        service.invoke(
          "onMicroBabyCrying",
          {"id": device.code},
        );
      } else if (predict.prediction != "Cry" && isMicroCrying) {
        isMicroCrying = false;
      }
    }));
  }

  static void onReceiveResponse(NotificationResponse details) {
    print(details.actionId);
    print(details.notificationResponseType);
    switch (details.notificationResponseType) {
      case NotificationResponseType.selectedNotification:
        AlarmPlayer.stop();
        break;

      case NotificationResponseType.selectedNotificationAction:
        switch (details.actionId) {
          case 'baby_crying_confirm':
            // Stop music
            AlarmPlayer.stop();
            break;
        }
        break;
      default:
        break;
    }
  }

  static Future<void> initialized() async {
    if (Platform.isIOS || Platform.isAndroid) {
      await flutterLocalNotificationsPlugin.initialize(
        const InitializationSettings(
          iOS: DarwinInitializationSettings(),
          android: AndroidInitializationSettings('ic_bg_service_small'),
        ),
        onDidReceiveNotificationResponse: onReceiveResponse,
        onDidReceiveBackgroundNotificationResponse: onReceiveResponse,
      );
    }

    await flutterLocalNotificationsPlugin
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
    await service.configure(
      androidConfiguration: AndroidConfiguration(
        // this will be executed when app is in foreground or background in separated isolate
        onStart: _onStart,

        // auto start service
        autoStart: true,
        isForegroundMode: true,

        notificationChannelId: 'tinyguard_foreground_service',
        initialNotificationTitle: 'TinyGuard alert service',
        initialNotificationContent: 'Initializing',
        foregroundServiceNotificationId: 888,
      ),
      iosConfiguration: IosConfiguration(
        // auto start service
        autoStart: true,

        // this will be executed when app is in foreground in separated isolate
        onForeground: _onStart,
      ),
    );
  }

  static void _onStart(ServiceInstance service) {
    DartPluginRegistrant.ensureInitialized();
    //if (service is AndroidServiceInstance) {
    //  service.setAsForegroundService();
    //}

    // Timer.periodic(Duration(seconds: 1), (timer) {
    //   flutterLocalNotificationsPlugin.show(
    //       888,
    //       'TinyGuard Alert',
    //       'Your baby seems to be crying!',
    //       NotificationDetails(
    //         android: AndroidNotificationDetails(
    //             'tinyguard_foreground', 'TinyGuard Foreground Service',
    //             icon: 'ic_bg_service_small',
    //             ongoing: true,
    //             actions: [
    //               AndroidNotificationAction("baby_crying_confirm", "Confirm",
    //                   showsUserInterface: true)
    //             ],
    //             subText:
    //                 "Camera with code: 'test' detected your baby is crying"),
    //       ));
    // });

    service.on("onCameraBabyCrying").listen((data) async {
      AlarmPlayer.play();
      final code = data?['id'] ?? '';

      if (data != null)
        flutterLocalNotificationsPlugin.show(
          888,
          'TinyGuard Alert',
          'The camera has detected that your baby is crying!\n' +
              DateFormat("yyyy-MM-dd h:mm:ss a").format(DateTime.now()),
          NotificationDetails(
            android: AndroidNotificationDetails(
              'tinyguard_foreground',
              'TinyGuard Foreground Service',
              icon: 'ic_bg_service_small',
              actions: [
                AndroidNotificationAction("baby_crying_confirm", "Confirm",
                    showsUserInterface: true)
              ],
              subText: "Camera $code",
              autoCancel: true,
            ),
          ),
        );
    });

    service.on("onMicroBabyCrying").listen((data) async {
      AlarmPlayer.play();
      final code = data?['id'] ?? '';

      if (data != null)
        flutterLocalNotificationsPlugin.show(
          888,
          'TinyGuard Alert',
          'The camera has detected that your baby is crying!',
          NotificationDetails(
            android: AndroidNotificationDetails(
                'tinyguard_foreground', 'TinyGuard Foreground Service',
                icon: 'ic_bg_service_small',
                ongoing: true,
                actions: [
                  AndroidNotificationAction("baby_crying_confirm", "Confirm",
                      showsUserInterface: true)
                ],
                subText: "Camera $code"),
          ),
        );
    });
  }
}

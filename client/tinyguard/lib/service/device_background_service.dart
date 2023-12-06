import 'dart:io';
import 'dart:ui';

import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:tinyguard/data/repository/device_repository.dart';

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

  static void addDevice(Device device) {
    _devices.add(device);
    device.image_predicts.stream.listen((predict) {
      if (predict.is_crying)
        service.invoke("onBabyCrying", {"id": device.code});
    });
  }

  static void onReceiveResponse(NotificationResponse details) {
    switch (details.notificationResponseType) {
      case NotificationResponseType.selectedNotification:
        break;

      case NotificationResponseType.selectedNotificationAction:
        switch (details.actionId) {
          case 'baby_crying_confirm':
            // Stop music

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

  @pragma("vm:entry-point")
  static void _onStart(ServiceInstance service) {
    DartPluginRegistrant.ensureInitialized();

    //if (service is AndroidServiceInstance) {
    //  service.setAsForegroundService();
    //}

    service.on("onBabyCrying").listen((data) {
      flutterLocalNotificationsPlugin.show(
        888,
        'TinyGuard Alert',
        'Y',
        const NotificationDetails(
          android: AndroidNotificationDetails(
              'tinyguard_foreground', 'TinyGuard Foreground Service',
              icon: 'ic_bg_service_small',
              ongoing: true,
              actions: [
                AndroidNotificationAction("baby_crying_confirm", "Confirm",
                    showsUserInterface: true)
              ]),
        ),
      );
    });
  }
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:tinyguard/page/first_setup_screen/ui/first_setup_screen.dart';
import 'package:tinyguard/page/main_screen/ui/main_screen.dart';

import 'package:tinyguard/page/monitor_screen/ui/monitor_screen.dart';
import 'package:tinyguard/page/splash_screen/splash1_screen.dart';
import 'package:tinyguard/page/splash_screen/splash2_screen.dart';
import 'package:tinyguard/page/splash_screen/splash3_screen.dart';
import 'package:tinyguard/util/container.dart';

void main() async {
  await ComponentContainer.ensureInit();

  runApp(const MainApp());
}

class Routes {
  static const String splash1 = '/splash1';
  static const String splash2 = '/splash2';
  static const String splash3 = '/splash3';

  static const String firstSetup = '/firstsetup';
  static const String dashboard = '/dashboard';
  static const String monitor = '/monitor';
  static final Map<String, Widget Function(BuildContext)> routes = {
    splash1: (context) {
      return Splash1Screen();
    },
    firstSetup: (context) {
      return FirstSetupScreen();
    },
    monitor: (context) {
      String urlLink = ModalRoute.of(context)?.settings.arguments as String;
      return MonitorScreen(urlLink: urlLink);
    }
  };
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: Routes.splash1,
      routes: Routes.routes,
    );
  }
}

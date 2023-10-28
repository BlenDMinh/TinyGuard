import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/src/widgets/placeholder.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:get/get.dart';
import 'package:get/get_core/src/get_main.dart';
import 'package:tinyguard/main.dart';
import 'package:tinyguard/util/bounding_box.dart';

import '../../../const/app_colors.dart';
import '../../../service/esp32_cam.dart';
import '../../../util/app_text_field.dart';
import '../../../util/container.dart';

class MonitorScreen extends StatefulWidget {
  final String urlLink;
  const MonitorScreen({super.key, required this.urlLink});

  @override
  State<MonitorScreen> createState() => _MonitorScreenState();
}

class _MonitorScreenState extends State<MonitorScreen> {
  @override
  void initState() {
    WidgetsFlutterBinding.ensureInitialized();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight, // Allow landscape right orientation
    ]);
    super.initState();
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    @override
    final videoService =
        ComponentContainer().get(Component.esp32Camera) as Esp32Camera;
    //videoService.bluetoothAddress = "55:65:AE:C8:CD:7C";
    return GestureDetector(
      onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
      child: WillPopScope(
        onWillPop: () => Future.value(true),
        child: Scaffold(
          backgroundColor: AppColors.blackBackground,
          body: Stack(
            children: [
              Container(
                alignment: Alignment.center,
                child: Mjpeg(
                  width: MediaQuery.of(context).size.width,
                  fit: BoxFit.fitWidth,
                  stream:
                      'https://blog.pregistry.com/wp-content/uploads/2018/04/AdobeStock_42898239.jpeg',
                  isLive: true,
                ),
              ),
              BoundingBox(
                x: 260,
                y: 0,
                height: 250,
                width: 270,
                isCrying: true,
              ),
              Positioned(
                bottom: 20.0,
                right: 20.0,
                child: FloatingActionButton(
                  backgroundColor: Colors.deepPurpleAccent,
                  onPressed: () {
                    Get.offAllNamed(Routes.firstSetup);
                  },
                  child: Icon(
                    Icons.add,
                    size: 35,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

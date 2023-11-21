import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:tinyguard/const/app_colors.dart';
import 'package:tinyguard/main_development.dart';
import 'package:tinyguard/ui/views/base/base_view.dart';
import 'package:tinyguard/widget/bounding_box.dart';
import 'package:tinyguard/widget/ui_button_transparent.dart';
import '../../../../service/esp32_cam.dart';
import '../../../../widget/container.dart';

class MonitorScreen extends StatefulWidget {
  final String urlLink;
  const MonitorScreen({super.key, required this.urlLink});

  @override
  State<MonitorScreen> createState() => _MonitorScreenState();
}

class _MonitorScreenState extends State<MonitorScreen> {
  bool isExpanded = false;

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
    return BaseView(
      mobileBuilder: (context) {
        return GestureDetector(
          onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
          child: Stack(
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
                confidence: 100,
              ),
              AnimatedPositioned(
                  top: isExpanded ? -20 : 0,
                  right: MediaQuery.of(context).size.width / 2.8,
                  duration: Duration(milliseconds: 200),
                  child: isExpanded
                      ? SizedBox.shrink()
                      : GestureDetector(
                          child: Container(
                            padding: EdgeInsets.symmetric(
                                horizontal: 16, vertical: 10),
                            decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.8),
                                borderRadius: BorderRadius.only(
                                    bottomLeft: Radius.circular(20),
                                    bottomRight: Radius.circular(20)),
                                border:
                                    Border.all(width: 1, color: Colors.white)),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Container(
                                  child: Row(
                                    children: [
                                      Icon(
                                        Icons.heart_broken,
                                        color: AppColors.lightPurple,
                                      ),
                                      Text(
                                        '100 bpm',
                                        style: TextStyle(
                                            fontSize: 18,
                                            color: Colors.black54,
                                            fontWeight: FontWeight.bold),
                                      )
                                    ],
                                  ),
                                ),
                                Container(
                                  width: 1,
                                  margin: EdgeInsets.symmetric(horizontal: 10),
                                  height: 30,
                                  color: Colors.black,
                                ),
                                Container(
                                  child: Row(
                                    children: [
                                      Icon(
                                        Icons.check_circle,
                                        color: AppColors.lightPurple,
                                      ),
                                      Text(
                                        '100 %',
                                        style: TextStyle(
                                            fontSize: 18,
                                            color: Colors.black54,
                                            fontWeight: FontWeight.bold),
                                      )
                                    ],
                                  ),
                                )
                              ],
                            ),
                          ),
                        )),
              AnimatedPositioned(
                bottom: 20.0,
                left: 20.0,
                duration: Duration(milliseconds: 200),
                child: UIButtonTransparent(
                  icon: isExpanded ? Icons.chevron_right : Icons.chevron_left,
                  onTap: () {
                    setState(() {
                      print(isExpanded.toString());
                      isExpanded = !isExpanded;
                    });
                  },
                ),
              ),
              AnimatedPositioned(
                bottom: 20.0,
                left: isExpanded ? 20 : 80.0,
                duration: Duration(milliseconds: 200),
                child: isExpanded
                    ? SizedBox.shrink()
                    : UIButtonTransparent(
                        icon: Icons.lock,
                        onTap: () {
                          setState(() {
                            isExpanded = !isExpanded;
                          });
                        },
                      ),
              ),
              AnimatedPositioned(
                bottom: 20.0,
                left: isExpanded ? 20 : 140.0,
                duration: Duration(milliseconds: 200),
                child: isExpanded
                    ? SizedBox.shrink()
                    : UIButtonTransparent(
                        icon: Icons.volume_off,
                        onTap: () {},
                      ),
              ),
              AnimatedPositioned(
                bottom: 20.0,
                left: isExpanded ? 20 : 200.0,
                duration: Duration(milliseconds: 200),
                child: isExpanded
                    ? SizedBox.shrink()
                    : UIButtonTransparent(
                        icon: Icons.camera_outlined,
                        onTap: () {
                          setState(() {
                            isExpanded = !isExpanded;
                          });
                        },
                      ),
              ),
              AnimatedPositioned(
                top: isExpanded ? 200 : 320,
                right: 20,
                duration: Duration(milliseconds: 200),
                child: isExpanded
                    ? SizedBox.shrink()
                    : UIButtonTransparent(
                        icon: Icons.mic,
                        onTap: () {
                          setState(() {
                            isExpanded = !isExpanded;
                          });
                        },
                      ),
              ),
            ],
          ),
        );
      },
    );
  }
}

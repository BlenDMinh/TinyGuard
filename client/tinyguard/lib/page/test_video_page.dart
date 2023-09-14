import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:flutter_vlc_player/flutter_vlc_player.dart';
import 'package:tinyguard/service/esp32_cam.dart';
import 'package:tinyguard/util/container.dart';

class TestVideoPage extends StatefulWidget {
  const TestVideoPage({super.key});

  @override
  State<StatefulWidget> createState() => _TestVideoPageState();
}

class _TestVideoPageState extends State<TestVideoPage> {
  @override
  Widget build(BuildContext context) {
    final videoService = ComponentContainer().get(Component.esp32CameraService)
        as Esp32CameraService;
    return Mjpeg(
      stream: videoService.url,
      isLive: true,
      // error: (contet, error, stack) => CircularProgressIndicator(),
    );
  }
}

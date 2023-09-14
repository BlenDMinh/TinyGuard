import 'package:flutter/material.dart';
import 'package:tinyguard/page/test_video_page.dart';
import 'package:tinyguard/util/container.dart';

void main() async {
  await ComponentContainer.ensureInit();
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(
          child: TestVideoPage(),
        ),
      ),
    );
  }
}

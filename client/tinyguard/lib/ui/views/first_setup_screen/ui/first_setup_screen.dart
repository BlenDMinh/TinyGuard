import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:tinyguard/widget/app_text_field.dart';

import '../../../../const/app_colors.dart';
import '../../../../main_development.dart';

class FirstSetupScreen extends StatefulWidget {
  const FirstSetupScreen({super.key});

  @override
  State<FirstSetupScreen> createState() => _FirstSetupScreenState();
}

class _FirstSetupScreenState extends State<FirstSetupScreen> {
  @override
  void initState() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
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
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.leanBack, overlays: [
      SystemUiOverlay.bottom,
      SystemUiOverlay.top,
    ]);

    final urlController = TextEditingController();
    return GestureDetector(
        onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
        child: WillPopScope(
            onWillPop: () => Future.value(false),
            child: Scaffold(
                appBar: AppBar(
                  title: Text(
                    "First setup",
                    style: TextStyle(fontSize: 25, color: Colors.grey[100]),
                  ),
                  backgroundColor: AppColors.blackBackground,
                ),
                backgroundColor: AppColors.blackBackground,
                body: SafeArea(
                    child: Container(
                        padding: EdgeInsets.symmetric(horizontal: 30),
                        child: Column(
                          children: [
                            Expanded(
                              flex: 1,
                              child: Column(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceAround,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text("Url please:",
                                        style: TextStyle(
                                            fontSize: 15,
                                            color: Colors.grey[100])),
                                    AppTextField(
                                      onChanged: (_) {},
                                      controller: urlController,
                                      radius: 10,
                                      backgroundColor: Colors.grey[100],
                                    ),
                                    GestureDetector(
                                      onTap: () => Get.toNamed(Routes.monitor,
                                          arguments: urlController.text),
                                      child: Container(
                                        width:
                                            MediaQuery.of(context).size.width /
                                                1,
                                        padding: EdgeInsets.all(15),
                                        decoration: BoxDecoration(
                                            borderRadius:
                                                BorderRadius.circular(15),
                                            color: Colors.deepPurpleAccent),
                                        child: Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: [
                                            Text(
                                              "Get started ",
                                              textAlign: TextAlign.center,
                                              style: TextStyle(
                                                  letterSpacing: 1,
                                                  fontSize: 19,
                                                  color: Colors.grey[100],
                                                  fontFamily: "Roboto",
                                                  fontWeight: FontWeight.bold),
                                            ),
                                            Icon(
                                              Icons.navigate_next,
                                              color: Colors.white,
                                              size: 30,
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ]),
                            ),
                            Expanded(
                              child: Container(),
                              flex: 3,
                            )
                          ],
                        ))))));
  }
}

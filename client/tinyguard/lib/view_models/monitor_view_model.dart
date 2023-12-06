import 'package:flutter/material.dart';
import 'package:tinyguard/data/repository/user_repository.dart';
import 'package:tinyguard/service/alarm_player.dart';
import 'package:tinyguard/view_models/base_view_model.dart';
import 'package:tinyguard/widget/bounding_box.dart';

class MonitorViewModel extends BaseViewModel {
  final UserRepository userRepository;
  late List<BoundingBox> listBoundingBox;

  bool isCrying = false;

  bool isExpanding = false;

  bool isPredicting = false;

  bool isMute = false;

  void setExpand() {
    isExpanding = !isExpanding;
    updateUI();
  }

  void setPredicting() {
    isPredicting = !isPredicting;
    debugPrint("PREDICT STATUS : " + isPredicting.toString());
    updateUI();
  }

  void setMute() {
    if (isMute == true) {
      AlarmPlayer.setVolume(0);
    } else {
      AlarmPlayer.setVolume(0.8);
    }
    updateUI();
  }

  void checkCrying() {}

  MonitorViewModel({required this.userRepository});
}

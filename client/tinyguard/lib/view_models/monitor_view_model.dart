import 'package:tinyguard/data/repository/user_repository.dart';
import 'package:tinyguard/view_models/base_view_model.dart';
import 'package:tinyguard/widget/bounding_box.dart';

class MonitorViewModel extends BaseViewModel {
  final UserRepository userRepository;
  late List<BoundingBox> listBoundingBox;

  bool isCrying = false;

  bool isExpanding = false;

  void setExpand() {
    isExpanding = !isExpanding;
    updateUI();
  }

  void checkCrying() {}

  MonitorViewModel({required this.userRepository});
}

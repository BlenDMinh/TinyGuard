import 'package:tinyguard/service/esp32_cam.dart';

enum Component { esp32CameraService }

class ComponentContainer {
  static final ComponentContainer _instance = ComponentContainer._();

  ComponentContainer._();

  factory ComponentContainer() {
    return ComponentContainer._instance;
  }

  static ensureInit() async {
    await _instance._init();
  }

  _init() async {
    container = {
      Component.esp32CameraService: await FakeEsp32CameraService.create()
    };
  }

  late Map<Component, dynamic> container;

  get(Component component) {
    return container[component];
  }
}

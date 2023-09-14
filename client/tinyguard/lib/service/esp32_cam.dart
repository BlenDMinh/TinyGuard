abstract class Esp32CameraService {
  String get url;
}

class FakeEsp32CameraService implements Esp32CameraService {
  String _url;
  FakeEsp32CameraService._() : _url = "http://192.168.5.166:81/stream";

  static create() async {
    var service = FakeEsp32CameraService._();
    return service;
  }

  @override
  String get url => _url;
}

class ImplementedEsp32CameraService implements Esp32CameraService {
  @override
  String get url => throw UnimplementedError();
}

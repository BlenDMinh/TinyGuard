import 'dart:async';

import 'package:flutter/material.dart';
import 'package:tinyguard/data/datasource/remote/entity/audio_predict_entity.dart';
import 'package:tinyguard/data/datasource/remote/entity/device_entity.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:tinyguard/data/datasource/remote/entity/image_predict_entity.dart';
import 'package:tinyguard/flavor_config.dart';

class Device {
  String code;
  IO.Socket _isocket;
  IO.Socket _asocket;
  final image_predicts = StreamController<ImagePredict>();
  final audio_streams = StreamController<AudioPredict>();

  Device(this.code)
      : _isocket = IO.io("${FlavorConfig.instance.baseApiUrl}/${code}_i",
            IO.OptionBuilder().setTransports(['websocket']).build()),
        _asocket = IO.io("${FlavorConfig.instance.baseApiUrl}/${code}_a") {
    debugPrint("${FlavorConfig.instance.baseApiUrl}/${code}_i");
    _isocket.connect();
    _asocket.connect();
    _isocket.on('connect', (data) {
      debugPrint("connected");
    });
    _isocket.on("ImagePrediction", (data) {
      image_predicts.sink.add(ImagePredict.fromJson(data));
      debugPrint(data.toString());
    });
    _asocket.on("AudioPrediction", (data) {
      audio_streams.sink.add(AudioPredict.fromJson(data));
      debugPrint(data.toString());
    });
  }

  factory Device.fromEntity(DeviceEntity entity) {
    return Device(entity.code);
  }
}

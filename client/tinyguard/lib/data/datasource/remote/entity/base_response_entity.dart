import 'package:tinyguard/data/datasource/remote/entity/common_info_entity.dart';

abstract class BaseResponseApiEntity {
  dynamic _body;
  CommonInfoEntity? _commonInfoEntity;

  BaseResponseApiEntity(dynamic body) {
    _body = _convertResponseJson(body);
    _setValueICommon();
    initialValue();
  }

  Map<String, dynamic> get body => _body as Map<String, dynamic>;

  CommonInfoEntity? get commonInfo => _commonInfoEntity;

  void initialValue();

  void _setValueICommon() {
    _commonInfoEntity = body['CommonInfo'] != null
        ? CommonInfoEntity.fromJson(
            body['CommonInfo'] as Map<String, dynamic>,
          )
        : null;
  }

  Map<String, dynamic> _convertResponseJson(dynamic responseJson) {
    return responseJson as Map<String, dynamic>;
  }
}

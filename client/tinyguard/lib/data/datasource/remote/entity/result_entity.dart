import 'package:tinyguard/data/datasource/remote/entity/item_entity.dart';

class ResultEntity {
  ItemEntity? item;

  ResultEntity({this.item});

  factory ResultEntity.fromJson(Map<String, dynamic> json) {
    return ResultEntity(
      item: json['Item'] != null
          ? ItemEntity.fromJson(
              json['Item'] as Map<String, dynamic>,
            )
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if (item != null) {
      data['Item'] = item!.toJson();
    }
    return data;
  }
}

class ItemEntity {
  final String? accessToken;
  final String? refreshToken;

  ItemEntity({required this.accessToken, required this.refreshToken});

  factory ItemEntity.fromJson(Map<String, dynamic> json) {
    return ItemEntity(
      accessToken: json['AccessToken'] as String?,
      refreshToken: json['RefreshToken'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['AccessToken'] = accessToken;
    data['RefreshToken'] = refreshToken;
    return data;
  }
}

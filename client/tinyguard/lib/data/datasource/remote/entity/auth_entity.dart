class AuthEntity {
  final String accessToken;
  final String refreshToken;

  AuthEntity({
    required this.accessToken,
    required this.refreshToken,
  });

  factory AuthEntity.fromJson(Map<String, dynamic> json) {
    return AuthEntity(
      accessToken: json['accessToken'] as String,
      refreshToken: json['refreshToken'] as String,
    );
  }
}

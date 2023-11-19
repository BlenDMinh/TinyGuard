import 'package:tinyguard/data/datasource/remote/api/api_client.dart';
import 'package:tinyguard/data/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/data/datasource/remote/entity/auth_entity.dart';

enum AuthRoute {
  login('/login');

  const AuthRoute(this.path);
  final String path;
}

class AuthAPIService {
  final APIClient client;

  AuthAPIService({required this.client});

  Future<AuthEntity> login(UserCredentials credentials) async {
    String path = AuthRoute.login.path;
    final response = await client.post(url: path, data: credentials.toJson());
    return AuthEntity.fromJson(response as Map<String, dynamic>);
  }
}

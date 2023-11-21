import 'package:tinyguard/data/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/data/datasource/remote/dto/user_register_credentials.dart';
import 'package:tinyguard/data/datasource/remote/entity/user_entity.dart';
import 'package:tinyguard/data/datasource/remote/service/auth_api_service.dart';
import 'package:tinyguard/data/datasource/remote/entity/auth_entity.dart';

abstract class UserRepository {
  Future<AuthEntity> login(UserCredentials credentials);
  Future<UserEntity> register(UserRegisterCredentials credentials);
}

class UserRepositoryImpl extends UserRepository {
  final AuthAPIService authAPIService;

  UserRepositoryImpl({
    required this.authAPIService,
  });

  @override
  Future<AuthEntity> login(UserCredentials credentials) {
    return authAPIService.login(credentials);
  }

  @override
  Future<UserEntity> register(UserRegisterCredentials credentials) {
    return authAPIService.register(credentials);
  }
}

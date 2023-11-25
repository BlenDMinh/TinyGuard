import 'package:flutter/material.dart';
import 'package:tinyguard/data/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/data/datasource/remote/entity/auth_entity.dart';
import 'package:tinyguard/data/repository/user_repository.dart';
import 'package:tinyguard/data/shared/constants.dart';
import 'package:tinyguard/data/shared_preferences/spref_auth_model.dart';
import 'package:tinyguard/utils/log_utils.dart';
import 'package:tinyguard/view_models.dart/base_view_model.dart';

class LogInViewModel extends BaseViewModel {
  final UserRepository userRepository;
  final SPrefAuthModel sPref;

  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  LogInViewModel({
    required this.userRepository,
    required this.sPref,
  });

  Future<void> onLoginPressed({
    VoidCallback? onSuccess,
    VoidCallback? onFailure,
  }) async {
    //try {
    debugPrint(emailController.text);
    debugPrint(passwordController.text);
    final entity = await userRepository.login(
      credentials: UserCredentials(
        email: emailController.text,
        password: passwordController.text,
      ),
    );
    onSuccessLogin(entity, onSuccess);
    //} on Exception catch (error) {
    //  LogUtils.d('LOGIN ERROR:  $runtimeType => $error');
    //  onFailure?.call();
    //}
  }

  Future<void> onSuccessLogin(
    AuthEntity entity,
    VoidCallback? onSuccess,
  ) async {
    await sPref.setAccessToken(
      value: entity.result?.accessToken ?? Constants.kEmptyString,
    );
    await sPref.setRefreshToken(
      value: entity.result?.refreshToken ?? Constants.kEmptyString,
    );
    onSuccess?.call();
  }
}

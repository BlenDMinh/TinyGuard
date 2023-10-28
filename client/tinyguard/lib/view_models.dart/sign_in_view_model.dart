import 'package:flutter/material.dart';
import 'package:tinyguard/data/datasource/remote/dto/user_credentials.dart';
import 'package:tinyguard/data/datasource/remote/entity/auth_entity.dart';
import 'package:tinyguard/data/repository/user_repository.dart';
import 'package:tinyguard/data/shared/constants.dart';
import 'package:tinyguard/data/shared_preferences/spref_auth_model.dart';
import 'package:tinyguard/utils/log_utils.dart';
import 'package:tinyguard/utils/validation_utils.dart';
import 'package:tinyguard/view_models.dart/base_view_model.dart';

class SignInViewModel extends BaseViewModel {
  final UserRepository userRepository;
  final SPrefAuthModel sPref;

  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  SignInViewModel({
    required this.userRepository,
    required this.sPref,
  });

  String _email = Constants.kEmptyString;
  String _password = Constants.kEmptyString;
  bool _isEnableBtn = false;

  String get email => _email;

  String get password => _password;

  bool get isEnableBtn => _isEnableBtn;

  void checkEnableButton() {
    if (emailController.text.isNotEmpty && passwordController.text.isNotEmpty) {
      _isEnableBtn = true;
    } else {
      _isEnableBtn = false;
    }
    updateUI();
  }

  void onEmailChange(String value) {
    _email = value;
    updateUI();
  }

  void onPasswordChange(String value) {
    _password = value;
    updateUI();
  }

  bool get isLoginButtonEnabled {
    return ValidationUtils.isValidPassword(_password) &&
        ValidationUtils.isEmail(_email);
  }

  Future<void> onLoginPressed({
    VoidCallback? onSuccess,
    VoidCallback? onFailure,
  }) async {
    try {
      final entity = await userRepository.login(
        UserCredentials(
          email: emailController.text,
          password: passwordController.text,
        ),
      );
      onSuccessLogin(entity, onSuccess);
    } on Exception catch (error) {
      LogUtils.d('Login $runtimeType => $error');
      onFailure?.call();
    }
  }

  Future<void> onSuccessLogin(
    AuthEntity entity,
    VoidCallback? onSuccess,
  ) async {
    await sPref.setAccessToken(
      value: entity.result?.item?.accessToken ?? Constants.kEmptyString,
    );
    await sPref.setRefreshToken(
      value: entity.result?.item?.refreshToken ?? Constants.kEmptyString,
    );
    onSuccess?.call();
  }
}
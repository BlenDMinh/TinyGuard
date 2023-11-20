class UserRegisterCredentials {
  final String username;
  final int age;
  final String phone_number;
  final String email;
  final String password;

  UserRegisterCredentials({
    required this.username,
    required this.age,
    required this.phone_number,
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'age': age,
      'phone_number': phone_number,
      'email': email,
      'password': password,
    };
  }
}

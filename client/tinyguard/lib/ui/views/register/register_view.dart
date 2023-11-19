import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tinyguard/ui/shared/already_have_an_account_acheck.dart';
import 'package:tinyguard/ui/shared/background.dart';
import 'package:tinyguard/ui/views/base/base_view.dart';
import 'package:tinyguard/ui/views/base/responsive.dart';
import 'components/sign_up_top_image.dart';

class RegisterView extends StatelessWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BaseView(
      resizeToAvoidBottomInset: true,
      mobileBuilder: (context) => Background(
        child: SingleChildScrollView(
          child: Responsive(
            mobile: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                const SignUpScreenTopImage(),
                Row(
                  children: [
                    Spacer(),
                    Expanded(
                      flex: 8,
                      child: Form(
                        child: Column(
                          children: [
                            TextFormField(
                              keyboardType: TextInputType.emailAddress,
                              textInputAction: TextInputAction.next,
                              cursorColor: Colors.black,
                              onSaved: (email) {},
                              decoration: InputDecoration(
                                hintText: "Your email",
                                prefixIcon: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Icon(Icons.person),
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.only(top: 16),
                              child: TextFormField(
                                textInputAction: TextInputAction.done,
                                obscureText: true,
                                cursorColor: Colors.black,
                                decoration: InputDecoration(
                                  hintText: "Your phone number",
                                  prefixIcon: Padding(
                                    padding: const EdgeInsets.all(16),
                                    child: Icon(Icons.phone),
                                  ),
                                ),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              child: TextFormField(
                                textInputAction: TextInputAction.done,
                                obscureText: true,
                                cursorColor: Colors.black,
                                decoration: InputDecoration(
                                  hintText: "Your password",
                                  prefixIcon: Padding(
                                    padding: const EdgeInsets.all(16),
                                    child: Icon(Icons.lock),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 8),
                            Hero(
                              tag: "login_btn",
                              child: ElevatedButton(
                                style: ButtonStyle(
                                    backgroundColor:
                                        MaterialStateProperty.all<Color>(
                                            Colors.deepPurpleAccent)),
                                onPressed: () {},
                                child: Text(
                                  "Sign up".toUpperCase(),
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            AlreadyHaveAnAccountCheck(
                              login: false,
                              press: () {
                                Get.back();
                              },
                            ),
                          ],
                        ),
                      ),
                    ),
                    Spacer(),
                  ],
                ),
                // const SocalSignUp()
              ],
            ),
          ),
        ),
      ),
    );
  }
}

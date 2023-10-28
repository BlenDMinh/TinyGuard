import 'package:flutter/material.dart';

class BoundingBox extends StatelessWidget {
  final double x;
  final double y;
  final double height;
  final double width;
  final bool isCrying;

  const BoundingBox({
    super.key,
    required this.x,
    required this.y,
    required this.height,
    required this.width,
    required this.isCrying,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("X: ${x}, Y: ${y}");
    return Transform(
      transform: Matrix4.translationValues(x, y, 0.0),
      child: Column(
        children: [
          Container(
            height: height,
            width: width,
            decoration: BoxDecoration(
              border: Border.all(
                width: 5,
                color: isCrying ? Colors.red : Colors.green,
              ),
            ),
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration:
                BoxDecoration(color: isCrying ? Colors.red : Colors.green),
            child: Text(
              isCrying ? 'Baby is crying' : "He's fine",
              style:
                  TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          )
        ],
      ),
    );
  }
}

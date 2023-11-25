class AudioPredict {
  final String prediction;

  AudioPredict(this.prediction);

  factory AudioPredict.fromJson(Map<String, dynamic> json) {
    return AudioPredict(json['prediction']);
  }
}

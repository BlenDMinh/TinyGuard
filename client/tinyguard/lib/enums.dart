enum Flavor {
  development,
  staging,
  production,
}

enum Level {
  error,
  warn,
  info,
  debug,
  trace,
}

enum BottomTabItem {
  home,
  search,
  favorite,
  profile,
}

enum City {
  osaka,
  kyoto,
  hyogo,
  shiga,
  nara,
  wakayama,
}

enum DatePickerEnum {
  year,
  month,
  day,
}

extension DatePickerEnumExtension on DatePickerEnum {
  int get getLengthRender {
    switch (this) {
      case DatePickerEnum.year:
        return 9001;
      case DatePickerEnum.month:
        return 12;
      case DatePickerEnum.day:
        return 31;
    }
  }

  bool get isYear => this == DatePickerEnum.year;
}

enum PaymentMethod {
  cash,
  visa,
}

enum UsePoint {
  fullPoint,
  manual,
}

import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';
import '../../data/models/alert.dart';

class LocalDB {
  static const _boxName = 'alerts';

  static Future<void> init() async {
    await Hive.initFlutter();
    await Hive.openBox(_boxName);
  }

  static Future<void> saveAlert(Alert alert) async {
    final box = Hive.box(_boxName);
    final key = '${alert.matchId}_${alert.timestamp.millisecondsSinceEpoch}';
    await box.put(key, jsonEncode(alert.toJson()));
  }

  static List<Alert> getAlerts() {
    final box = Hive.box(_boxName);
    return box.values
        .map((raw) => raw is String ? Alert.fromJson(jsonDecode(raw)) : null)
        .whereType<Alert>()
        .toList()
      ..sort((a, b) => b.timestamp.compareTo(a.timestamp));
  }
}

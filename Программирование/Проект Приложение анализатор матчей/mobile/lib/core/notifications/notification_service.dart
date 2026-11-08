import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../../data/models/alert.dart';

class NotificationService {
  final FlutterLocalNotificationsPlugin _local = FlutterLocalNotificationsPlugin();

  Future<void> init() async {
    await _local.initialize(const InitializationSettings(
      android: AndroidInitializationSettings('@mipmap/ic_launcher'),
    ));
  }

  Future<void> showAlertNotification(Alert alert) async {
    await _local.show(
      alert.hashCode,
      alert.conditionName,
      alert.description.length > 200
          ? '${alert.description.substring(0, 200)}...'
          : alert.description,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'alerts_channel',
          'Sports Alerts',
          importance: Importance.high,
          priority: Priority.high,
        ),
      ),
    );
  }
}

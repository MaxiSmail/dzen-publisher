import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app/app.dart';
import 'core/notifications/notification_service.dart';
import 'core/storage/local_db.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await LocalDB.init();
  await NotificationService().init();
  runApp(const ProviderScope(child: AnalizatorApp()));
}

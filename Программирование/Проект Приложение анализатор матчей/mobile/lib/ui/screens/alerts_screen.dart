import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/alert_provider.dart';
import '../widgets/alert_tile.dart';

class AlertsScreen extends ConsumerWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final alerts = ref.watch(alertListProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('История алертов')),
      body: alerts.isEmpty
          ? const Center(child: Text('Нет алертов'))
          : ListView.builder(
              itemCount: alerts.length,
              itemBuilder: (_, i) => AlertTile(alert: alerts[i]),
            ),
    );
  }
}

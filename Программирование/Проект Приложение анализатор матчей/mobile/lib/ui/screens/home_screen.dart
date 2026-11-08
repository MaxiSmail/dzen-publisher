import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/alert_provider.dart';
import '../widgets/alert_tile.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final alerts = ref.watch(alertListProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analizator'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () => context.push('/alerts'),
          ),
        ],
      ),
      body: alerts.isEmpty
          ? const Center(child: Text('Ожидание алертов...'))
          : ListView.builder(
              itemCount: alerts.length,
              itemBuilder: (_, i) => AlertTile(alert: alerts[i]),
            ),
    );
  }
}

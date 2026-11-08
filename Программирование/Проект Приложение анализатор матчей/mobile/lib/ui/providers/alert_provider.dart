import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/network/websocket_client.dart';
import '../../core/notifications/notification_service.dart';
import '../../data/models/alert.dart';
import '../../data/repositories/alert_repository.dart';
import '../../core/storage/local_db.dart';

final webSocketProvider = Provider<WebSocketClient>((ref) {
  final ws = WebSocketClient();
  ref.onDispose(() => ws.disconnect());
  return ws;
});

final alertRepositoryProvider = Provider<AlertRepository>((ref) {
  return AlertRepository();
});

final alertListProvider = StateNotifierProvider<AlertListNotifier, List<Alert>>((ref) {
  final repo = ref.watch(alertRepositoryProvider);
  final ws = ref.watch(webSocketProvider);
  return AlertListNotifier(repo, ws);
});

class AlertListNotifier extends StateNotifier<List<Alert>> {
  final AlertRepository _repo;
  final WebSocketClient _ws;
  final NotificationService _notif = NotificationService();
  StreamSubscription? _sub;
  Timer? _pollTimer;

  AlertListNotifier(this._repo, this._ws) : super([]) {
    _init();
  }

  Future<void> _init() async {
    try {
      final cached = LocalDB.getAlerts();
      if (cached.isNotEmpty) state = cached;
    } catch (_) {}

    try {
      final remote = await _repo.fetchRecent();
      state = remote;
    } catch (_) {}

    _ws.connect('ws://localhost:8000/ws/matches');
    _sub = _ws.alertStream.listen((alert) {
      try {
        LocalDB.saveAlert(alert);
      } catch (_) {}
      _notif.showAlertNotification(alert);
      state = [alert, ...state].take(200).toList();
    });

    _pollTimer = Timer.periodic(const Duration(seconds: 30), (_) async {
      try {
        final remote = await _repo.fetchRecent(since: state.isNotEmpty ? state.first.timestamp : null);
        if (remote.isNotEmpty) {
          for (final alert in remote) {
            if (!state.any((a) => a.matchId == alert.matchId && a.timestamp == alert.timestamp)) {
              state = [alert, ...state].take(200).toList();
            }
          }
        }
      } catch (_) {}
    });
  }

  @override
  void dispose() {
    _sub?.cancel();
    _pollTimer?.cancel();
    super.dispose();
  }
}

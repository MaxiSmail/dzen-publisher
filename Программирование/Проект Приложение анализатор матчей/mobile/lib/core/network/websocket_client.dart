import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../../data/models/alert.dart';

class WebSocketClient {
  WebSocketChannel? _channel;
  StreamSubscription? _streamSub;
  StreamController<Alert> _alertController = StreamController<Alert>.broadcast();
  Timer? _reconnectTimer;
  String _url = '';

  Stream<Alert> get alertStream => _alertController.stream;

  void connect(String url) {
    _url = url;
    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));
      _streamSub = _channel!.stream.listen(
        (raw) {
          try {
            final map = jsonDecode(raw) as Map<String, dynamic>;
            _alertController.add(Alert.fromJson(map));
          } catch (_) {}
        },
        onDone: _scheduleReconnect,
        onError: (_) => _scheduleReconnect(),
      );
    } catch (_) {
      _scheduleReconnect();
    }
  }

  void _scheduleReconnect() {
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(const Duration(seconds: 5), () => connect(_url));
  }

  void disconnect() {
    _reconnectTimer?.cancel();
    _streamSub?.cancel();
    _channel?.sink.close();
    if (!_alertController.isClosed) {
      _alertController.close();
    }
  }

  void reset() {
    disconnect();
    _alertController = StreamController<Alert>.broadcast();
  }
}

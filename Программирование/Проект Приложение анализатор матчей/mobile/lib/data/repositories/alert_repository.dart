import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/alert.dart';

class AlertRepository {
  final String baseUrl;

  AlertRepository({this.baseUrl = 'http://localhost:8000'});

  final Duration _timeout = const Duration(seconds: 10);

  Future<List<Alert>> fetchRecent({int limit = 50, DateTime? since}) async {
    final params = <String, String>{'limit': limit.toString()};
    if (since != null) {
      params['since'] = since.toIso8601String();
    }
    final uri = Uri.parse('$baseUrl/alerts').replace(queryParameters: params);
    try {
      final resp = await http.get(uri).timeout(_timeout);
      if (resp.statusCode != 200) return [];
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      final list = body['alerts'] as List<dynamic>? ?? [];
      return list.map((e) => Alert.fromJson(e as Map<String, dynamic>)).toList();
    } catch (_) {
      return [];
    }
  }

  Future<List<Alert>> fetchByMatch(String matchId) async {
    final uri = Uri.parse('$baseUrl/alerts/${Uri.encodeComponent(matchId)}');
    try {
      final resp = await http.get(uri).timeout(_timeout);
      if (resp.statusCode != 200) return [];
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      final list = body['alerts'] as List<dynamic>? ?? [];
      return list.map((e) => Alert.fromJson(e as Map<String, dynamic>)).toList();
    } catch (_) {
      return [];
    }
  }
}

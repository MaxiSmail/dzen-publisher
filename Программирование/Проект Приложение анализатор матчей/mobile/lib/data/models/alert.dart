class Alert {
  final String matchId;
  final String conditionName;
  final double edge;
  final String description;
  final DateTime timestamp;
  final Map<String, dynamic>? matchSnapshot;

  const Alert({
    required this.matchId,
    required this.conditionName,
    required this.edge,
    required this.description,
    required this.timestamp,
    this.matchSnapshot,
  });

  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      matchId: json['match_id'] as String? ?? '',
      conditionName: json['condition_name'] as String? ?? '',
      edge: (json['edge'] as num?)?.toDouble() ?? 0.0,
      description: json['description'] as String? ?? '',
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'] as String)
          : DateTime.now(),
      matchSnapshot: json['match'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() => {
        'match_id': matchId,
        'condition_name': conditionName,
        'edge': edge,
        'description': description,
        'timestamp': timestamp.toIso8601String(),
        'match': matchSnapshot,
      };

  String get edgePercent => '${(edge * 100).toStringAsFixed(1)}%';
}

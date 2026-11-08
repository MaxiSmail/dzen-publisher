class MatchEvent {
  final String matchId;
  final String homeTeam;
  final String awayTeam;
  final int homeScore;
  final int awayScore;
  final int minute;
  final double possessionHome;
  final double possessionAway;
  final int dangerousAttacksHome;
  final int dangerousAttacksAway;

  const MatchEvent({
    required this.matchId,
    required this.homeTeam,
    required this.awayTeam,
    required this.homeScore,
    required this.awayScore,
    required this.minute,
    required this.possessionHome,
    required this.possessionAway,
    required this.dangerousAttacksHome,
    required this.dangerousAttacksAway,
  });

  factory MatchEvent.fromJson(Map<String, dynamic> json) {
    return MatchEvent(
      matchId: json['match_id'] as String? ?? '',
      homeTeam: json['home_team'] as String? ?? '',
      awayTeam: json['away_team'] as String? ?? '',
      homeScore: json['home_score'] as int? ?? 0,
      awayScore: json['away_score'] as int? ?? 0,
      minute: json['minute'] as int? ?? 0,
      possessionHome: (json['possession_home'] as num?)?.toDouble() ?? 50.0,
      possessionAway: (json['possession_away'] as num?)?.toDouble() ?? 50.0,
      dangerousAttacksHome: json['dangerous_attacks_home'] as int? ?? 0,
      dangerousAttacksAway: json['dangerous_attacks_away'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {
        'match_id': matchId,
        'home_team': homeTeam,
        'away_team': awayTeam,
        'home_score': homeScore,
        'away_score': awayScore,
        'minute': minute,
        'possession_home': possessionHome,
        'possession_away': possessionAway,
        'dangerous_attacks_home': dangerousAttacksHome,
        'dangerous_attacks_away': dangerousAttacksAway,
      };
}

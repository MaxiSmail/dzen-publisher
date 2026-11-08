import 'package:flutter/material.dart';
import '../../data/models/match_event.dart';

class MatchCard extends StatelessWidget {
  final MatchEvent match;

  const MatchCard({super.key, required this.match});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(child: Text(match.homeTeam, style: const TextStyle(fontWeight: FontWeight.bold))),
                Text('${match.homeScore} : ${match.awayScore}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                Expanded(child: Text(match.awayTeam, textAlign: TextAlign.end, style: const TextStyle(fontWeight: FontWeight.bold))),
              ],
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: (match.minute / 90.0).clamp(0.0, 1.0)),
            Text('${match.minute}\' | Владение: ${match.possessionHome.toStringAsFixed(0)}% / ${match.possessionAway.toStringAsFixed(0)}%'),
          ],
        ),
      ),
    );
  }
}

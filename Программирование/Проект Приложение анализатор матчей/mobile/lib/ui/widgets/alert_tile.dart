import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../data/models/alert.dart';

class AlertTile extends StatelessWidget {
  final Alert alert;

  const AlertTile({super.key, required this.alert});

  @override
  Widget build(BuildContext context) {
    final dateStr = DateFormat('HH:mm:ss').format(alert.timestamp);
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _colorForCondition(alert.conditionName),
          child: Text(
            alert.conditionName.isNotEmpty ? alert.conditionName.substring(0, 1) : '?',
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
        title: Text(alert.conditionName, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(alert.description, maxLines: 2, overflow: TextOverflow.ellipsis),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(alert.edgePercent, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.greenAccent)),
            Text(dateStr, style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ),
    );
  }

  Color _colorForCondition(String name) {
    if (name.contains('HOME')) return Colors.blue;
    if (name.contains('AWAY')) return Colors.orange;
    if (name.contains('OVER')) return Colors.purple;
    return Colors.grey;
  }
}

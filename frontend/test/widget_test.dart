import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ai_planner/features/gamification/presentation/cloud_widget.dart';

void main() {
  testWidgets('CloudWidget displays correct icon for state', (WidgetTester tester) async {
    // 1. Clear Sky
    await tester.pumpWidget(const MaterialApp(home: CloudWidget(state: CloudState.clear)));
    expect(find.byIcon(Icons.cloud_queue), findsOneWidget);

    // 2. Stormy
    await tester.pumpWidget(const MaterialApp(home: CloudWidget(state: CloudState.storm)));
    expect(find.byIcon(Icons.thunderstorm), findsOneWidget);
  });
}

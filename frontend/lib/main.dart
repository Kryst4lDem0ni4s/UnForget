import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';

void main() {
  runApp(const AIPlannerApp());
}

class AIPlannerApp extends StatelessWidget {
  const AIPlannerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SkyPlan',
      theme: AppTheme.light(),
      home: Scaffold(
        appBar: AppBar(title: const Text('SkyPlan')),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.cloud, size: 100, color: Colors.blue),
              SizedBox(height: 20),
              Text('Welcome to SkyPlan', style: TextStyle(fontSize: 24)),
            ],
          ),
        ),
      ),
      debugShowCheckedModeBanner: false,
    );
  }
}

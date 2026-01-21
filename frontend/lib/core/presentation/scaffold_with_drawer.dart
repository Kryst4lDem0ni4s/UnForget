import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'app_drawer.dart';

class ScaffoldWithDrawer extends StatelessWidget {
  final Widget child;

  const ScaffoldWithDrawer({required this.child, super.key});

  @override
  Widget build(BuildContext context) {
    // Determine title based on location if possible, but for now we keep it dynamic or simple
    // Actually, we can just have the AppBar here or let individual screens have it.
    // The user requested "Hamburger menu absent from all UIs other than home screen"
    // So we MUST put the AppBar here to guarantee it on all screens.
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('SkyPlan'), // Dynamic titles would be better, but MVP first
        centerTitle: true,
      ),
      drawer: const AppDrawer(),
      body: child,
    );
  }
}

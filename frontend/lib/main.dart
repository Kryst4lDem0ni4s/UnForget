import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:ai_planner/core/theme/app_theme.dart';
import 'package:ai_planner/core/router/app_router.dart';

void main() {
  runApp(const ProviderScope(child: AIPlannerApp()));
}

class AIPlannerApp extends ConsumerWidget {
  const AIPlannerApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Expecting routerProvider from generated code
    final routerConfig = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'AI Planner',
      theme: AppTheme.light(),
      routerConfig: routerConfig,
      debugShowCheckedModeBanner: false,
    );
  }
}

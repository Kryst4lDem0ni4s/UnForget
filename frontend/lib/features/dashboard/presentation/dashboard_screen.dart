import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../gamification/presentation/cloud_widget.dart';
import '../../gamification/data/gamification_provider.dart';
import 'widgets/sync_visualizer.dart';
import 'widgets/add_task_button.dart';
import '../../../core/api/sync_provider.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  // Intead of local state, we watch the provider
  
  @override
  Widget build(BuildContext context) {
    final cloudStateAsync = ref.watch(cloudStateProvider);
    // Rename to avoid conflict with the imported 'cloudState' function
    final currentCloudState = cloudStateAsync.valueOrNull ?? CloudState.clear;
    final isSyncing = ref.watch(syncStatusProvider);
    
    // Return only the body content, Scaffold is provided by ShellRoute
    return LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth > 800) {
            return _buildDesktopLayout(currentCloudState);
          } else {
            return _buildMobileLayout(currentCloudState);
          }
        },
    );
  }

  Widget _buildDesktopLayout(CloudState state) {
    return Column(
      children: [
        // Top: Large Gamification Cloud
        Expanded(
          flex: 2,
          child: Center(
             child: Column(
               mainAxisAlignment: MainAxisAlignment.center,
               children: [
                 CloudWidget(state: state, size: 300),
                 const SizedBox(height: 20),
                 Text(
                   state == CloudState.storm ? "Storm Approaching!" : "Clear Skies",
                   style: Theme.of(context).textTheme.headlineMedium,
                 ),
               ],
             ),
          ),
        ),
        // Center: Interactive Add Task (Small Cloud)
        Expanded(
          flex: 1,
          child: Center(
            child: Column(
              children: [
                const Text("Add a new cloud", style: TextStyle(color: Colors.grey)),
                const SizedBox(height: 16),
                // Reusing AddTaskButton, simplified
                const AddTaskButton(isMobile: true), // Using mobile version (FAB style) as "Small Cloud"
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMobileLayout(CloudState state) {
    return Column(
      children: [
        const SizedBox(height: 40),
        // Top: Large Cloud
        CloudWidget(state: state, size: 250),
        const SizedBox(height: 20),
        Text(
           state == CloudState.storm ? "Storm Approaching!" : "Clear Skies",
           style: Theme.of(context).textTheme.headlineSmall,
        ),
        
        const Spacer(),
        
        // Center: Interactive Add Task
        const Text("Tap to add task", style: TextStyle(color: Colors.grey)),
        const SizedBox(height: 16),
        const AddTaskButton(isMobile: true),
        
        const Spacer(),
      ],
    );
  }
}



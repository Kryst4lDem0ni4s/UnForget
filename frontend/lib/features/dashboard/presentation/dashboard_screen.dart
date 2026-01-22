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
    return Stack(
      children: [
        // Background could be added here
        
        Column(
          children: [
            const SizedBox(height: 60), // Space for top bar
            // Top: Large Hero Cloud (Status)
            Expanded(
              flex: 4,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Hero(
                    tag: 'hero_cloud',
                    child: CloudWidget(state: state, size: 280),
                  ),
                  const SizedBox(height: 24),
                  Text(
                     state == CloudState.storm ? "Storm Approaching!" : "Clear Skies",
                     style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                       fontWeight: FontWeight.bold,
                       color: state == CloudState.storm ? Colors.red.shade700 : Colors.blue.shade700,
                     ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "You're doing great, adventurer!",
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Colors.grey.shade600
                    ),
                  )
                ],
              ),
            ),
            
            // Center/Bottom area: Action Cloud
            Expanded(
              flex: 3,
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text("Tap cloud to plan", style: TextStyle(color: Colors.grey, letterSpacing: 1.2)),
                    const SizedBox(height: 20),
                    // The "Small Cloud" interactive button
                    GestureDetector(
                      onTap: () => showDialog(
                        context: context, 
                        builder: (context) => const AddTaskDialog()
                      ),
                      child: Container(
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: Colors.blue.withOpacity(0.2),
                              blurRadius: 20,
                              spreadRadius: 5,
                            )
                          ]
                        ),
                        child: const CloudWidget(state: CloudState.clear, size: 100),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}



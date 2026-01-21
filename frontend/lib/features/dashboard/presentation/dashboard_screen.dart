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
    final cloudState = cloudStateAsync.valueOrNull ?? CloudState.clear;
    final isSyncing = ref.watch(syncStatusProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('SkyPlan'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.read(syncStatusProvider.notifier).startSync();
              Future.delayed(const Duration(seconds: 3), () {
                ref.read(syncStatusProvider.notifier).endSync();
              });
            },
          ),
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
        ],
      ),
      drawer: const _AppDrawer(),
      body: LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth > 800) {
            return _buildDesktopLayout();
          } else {
            return _buildMobileLayout();
          }
        },
      ),
      floatingActionButton: LayoutBuilder(
        builder: (context, constraints) {
          // Only show FAB on mobile
          if (constraints.maxWidth <= 800) {
            return const AddTaskButton(isMobile: true);
          }
          return const SizedBox.shrink();
        },
      ),
      bottomNavigationBar: isSyncing 
        ? Padding(
            padding: const EdgeInsets.only(bottom: 80.0),
            child: Center(child: SyncVisualizer(isSyncing: isSyncing)),
          )
        : null,
    );
  }

  Widget _buildDesktopLayout() {
    return Row(
      children: [
        // Main Area (Gamification)
        Expanded(
          flex: 2,
          child: Center(
             child: Column(
               mainAxisAlignment: MainAxisAlignment.center,
               children: [
                 CloudWidget(state: cloudState, size: 300),
                 const SizedBox(height: 20),
                 Text(
                   cloudState == CloudState.storm ? "Storm Approaching!" : "Clear Skies",
                   style: Theme.of(context).textTheme.headlineMedium,
                 ),
               ],
             ),
          ),
        ),
        // Side Panel (Quick Add Task)
        Expanded(
          flex: 1,
          child: Container(
            color: Colors.white.withOpacity(0.5),
            padding: const EdgeInsets.all(24),
            child: const Center(
              child: AddTaskButton(isMobile: false),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMobileLayout() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CloudWidget(state: cloudState, size: 200),
          const SizedBox(height: 32),
          Text(
            "Your Day is Clear",
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            "Tap the cloud to plan",
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey),
          ),
        ],
      ),
    );
  }
}

class _AppDrawer extends StatelessWidget {
  const _AppDrawer();

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Icon(Icons.cloud, color: Colors.white, size: 48),
                const SizedBox(height: 10),
                Text('SkyPlan Menu', style: Theme.of(context).textTheme.titleLarge?.copyWith(color: Colors.white)),
              ],
            ),
          ),
          ListTile(
            leading: const Icon(Icons.dashboard_outlined),
            title: const Text('Home (Cloud View)'),
            onTap: () {
               context.pop(); // Close drawer
               context.go('/');
            },
          ),
          ListTile(
            leading: const Icon(Icons.calendar_month_outlined),
            title: const Text('Calendar Schedule'),
            onTap: () {
               context.pop();
               context.go('/calendar');
            },
          ),
          ListTile(
            leading: const Icon(Icons.check_circle_outline),
            title: const Text('To-Do List'),
            onTap: () {
               context.pop();
               context.go('/tasks');
            },
          ),
          ListTile(
            leading: const Icon(Icons.person_outline),
            title: const Text('Adventurer Profile'),
            onTap: () {
               context.pop();
               context.go('/profile');
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.settings_outlined),
            title: const Text('Settings'),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}

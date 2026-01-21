import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

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

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../gamification/presentation/cloud_widget.dart';
import '../../tasks/presentation/add_task_dialog.dart';

class AddTaskButton extends ConsumerWidget {
  final bool isMobile;
  
  const AddTaskButton({super.key, this.isMobile = false});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    if (isMobile) {
      return FloatingActionButton(
        onPressed: () => showDialog(
          context: context, 
          builder: (context) => const AddTaskDialog()
        ),
        tooltip: 'Add Task',
        backgroundColor: Colors.white,
        child: const SizedBox(
            width: 32, 
            height: 32, 
            child: CloudWidget(state: CloudState.clear, size: 32)
        ),
      );
    }
    
    // Desktop version - Large card
    return Container(
      constraints: const BoxConstraints(maxWidth: 400),
      child: Card(
        elevation: 8,
        shadowColor: Theme.of(context).primaryColor.withOpacity(0.2),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        child: InkWell(
          onTap: () => showDialog(
            context: context,
            builder: (context) => const AddTaskDialog(),
          ),
          borderRadius: BorderRadius.circular(24),
          child: Padding(
            padding: const EdgeInsets.all(40.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Use the Cloud Widget here for branding
                const CloudWidget(state: CloudState.clear, size: 100),
                const SizedBox(height: 24),
                Text(
                  'Add New Task',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColor,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                Text(
                  'Plan your day with the clouds.',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[600],
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                FilledButton.icon( // Modern button
                FilledButton.icon( // Modern button
                    onPressed: () => showDialog(
                      context: context,
                      builder: (context) => const AddTaskDialog(),
                    ),
                    icon: const Icon(Icons.add),
                    label: const Text("Create Entry"),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}

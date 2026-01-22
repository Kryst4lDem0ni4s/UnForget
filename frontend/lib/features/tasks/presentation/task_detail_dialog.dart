import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../tasks/data/task_repository.dart';

class TaskDetailDialog extends ConsumerWidget {
  final Task task;

  const TaskDetailDialog({required this.task, super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDone = task.status == 'completed';

    return Dialog(
       shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
       child: Container(
         padding: const EdgeInsets.all(24),
         constraints: const BoxConstraints(maxWidth: 500),
         child: Column(
           mainAxisSize: MainAxisSize.min,
           crossAxisAlignment: CrossAxisAlignment.start,
           children: [
             Row(
               mainAxisAlignment: MainAxisAlignment.spaceBetween,
               children: [
                 Expanded(
                   child: Text(
                     task.title, 
                     style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                       decoration: isDone ? TextDecoration.lineThrough : null,
                     )
                   ),
                 ),
                 IconButton(
                   icon: const Icon(Icons.close),
                   onPressed: () => context.pop(),
                 )
               ],
             ),
             const Divider(),
             const SizedBox(height: 16),
             
             // Details
             _buildSection(context, "Context", task.contextNotes ?? "No additional context."),
             const SizedBox(height: 16),
             _buildSection(context, "AI Reasoning", task.aiReasoning ?? "Manual entry."),
             const SizedBox(height: 16),
             
             // Actions
             Row(
               mainAxisAlignment: MainAxisAlignment.end,
               children: [
                 TextButton.icon(
                   icon: const Icon(Icons.delete, color: Colors.red),
                   label: const Text("Remove", style: TextStyle(color: Colors.red)),
                   onPressed: () async {
                      try {
                        await ref.read(taskRepositoryProvider).deleteTask(task.id);
                        if (context.mounted) {
                          context.pop();
                          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Task Removed")));
                          // Force refresh of task list
                          ref.invalidate(taskListProvider);
                        }
                      } catch (e) {
                         if (context.mounted) {
                           ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
                         }
                      }
                   },
                 ),
                 const SizedBox(width: 8),
                 if (!isDone)
                   FilledButton.icon(
                     icon: const Icon(Icons.check),
                     label: const Text("Complete"),
                     onPressed: () async {
                        try {
                          final updatedTask = task.copyWith(status: 'completed');
                          await ref.read(taskRepositoryProvider).updateTask(updatedTask);
                          if (context.mounted) {
                            context.pop();
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text("Task Completed! +10 XP"), 
                                backgroundColor: Colors.green
                              )
                            );
                            // Force refresh
                            ref.invalidate(taskListProvider);
                          }
                        } catch (e) {
                           if (context.mounted) {
                             ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
                           }
                        }
                     },
                   ),
               ],
             )
           ],
         ),
       ),
    );
  }

  Widget _buildSection(BuildContext context, String title, String content) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: TextStyle(color: Theme.of(context).colorScheme.primary, fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        Text(content, style: Theme.of(context).textTheme.bodyMedium),
      ],
    );
  }
}

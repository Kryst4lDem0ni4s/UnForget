import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../tasks/data/task_repository.dart';
import 'task_detail_dialog.dart';
import 'add_task_dialog.dart';

class TaskListScreen extends ConsumerWidget {
  const TaskListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
     final tasksAsync = ref.watch(taskListProvider);

     // No Scaffold here - relying on ShellRoute's ScaffoldWithDrawer
     // We just return the body.
     // However, we need a FAB. The parent Scaffold can't easily switch FABs based on child.
     // A common pattern with ShellRoute is for the child to use a Scaffold ONLY for FAB/Snackbars
     // but transparency for AppBar/Drawer.
     // OR we move the FAB to the dashboard/add-task flow as requested.
     // User requirement: "A new task should be a small cloud at the center of the screen that can be clicked." on DASHBOARD.
     // On TaskList, maybe we don't need a FAB if the dashboard is the primary way?
     // Or we keep it but ensure AppBar isn't duplicated.
     
     // Let's use a Scaffold but with backgroundColor transparent and NO AppBar/Drawer
     // This allows FAB usage without hiding parent AppBar (if we don't define one here).
     
     return Scaffold(
       backgroundColor: Colors.transparent, // Let parent background show
       // No AppBar - allows parent AppBar to show
       body: tasksAsync.when(
         data: (tasks) {
           if (tasks.isEmpty) {
             return const Center(
               child: Text("No clouds in the sky yet."),
             );
           }
           return ListView.builder(
             padding: const EdgeInsets.all(16),
             itemCount: tasks.length,
             itemBuilder: (context, index) {
               final task = tasks[index];
               final isDone = task.status == 'completed';
               return Card(
                 child: ListTile(
                   leading: Icon(
                     isDone ? Icons.check_circle : Icons.circle_outlined, 
                     color: isDone ? Colors.green : Colors.grey
                   ),
                   title: Text(
                     task.title,
                     style: TextStyle(
                       decoration: isDone ? TextDecoration.lineThrough : null,
                       color: isDone ? Colors.grey : null,
                     ),
                   ),
                   subtitle: Text(task.priority ?? "Normal"),
                   onTap: () => showDialog(
                     context: context,
                     builder: (context) => TaskDetailDialog(task: task),
                   ),
                 ),
               );
             },
           );
         },
         loading: () => const Center(child: CircularProgressIndicator()),
         error: (err, stack) => Center(child: Text('Error: $err')),
       ),
       floatingActionButton: FloatingActionButton(
         onPressed: () => showDialog(
           context: context, 
           builder: (context) => const AddTaskDialog()
         ),
         child: const Icon(Icons.add),
       ),
     );
  }
}

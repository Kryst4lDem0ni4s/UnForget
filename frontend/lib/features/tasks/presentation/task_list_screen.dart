import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class TaskListScreen extends StatelessWidget {
  const TaskListScreen({super.key});

  @override
  Widget build(BuildContext context) {
     return Scaffold(
       appBar: AppBar(title: const Text('To-Do List')),
       body: ListView(
         padding: const EdgeInsets.all(16),
         children: [
           Card(
             child: ListTile(
               leading: const Icon(Icons.circle_outlined),
               title: const Text("Setup AI Planner"),
               subtitle: const Text("High Priority"),
               onTap: () {},
             ),
           ),
           Card(
             child: ListTile(
               leading: const Icon(Icons.check_circle, color: Colors.green),
               title: const Text("Complete Backend"),
               subtitle: const Text("Done"),
             ),
           ),
         ],
       ),
       floatingActionButton: FloatingActionButton(
         onPressed: () => context.go('/add-task'),
         child: const Icon(Icons.add),
       ),
     );
  }
}

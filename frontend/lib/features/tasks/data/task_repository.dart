import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../../core/api/api_client.dart';
import 'package:dio/dio.dart';

part 'task_repository.g.dart';

@riverpod
Future<List<Task>> taskList(TaskListRef ref) async {
  final repo = ref.watch(taskRepositoryProvider);
  return repo.getTasks();
}

@riverpod
TaskRepository taskRepository(TaskRepositoryRef ref) {
  return TaskRepository(ref.watch(apiClientProvider));
}

class TaskRepository {
  final Dio _dio;
  TaskRepository(this._dio);

  Future<List<Task>> getTasks() async {
    final response = await _dio.get('/tasks');
    final List data = response.data;
    return data.map((json) => Task.fromJson(json)).toList();
  }

  Future<int> getPendingTaskCount() async {
    final tasks = await getTasks();
    return tasks.where((t) => t.status != 'completed').length;
  }
  
  // Mock delete/update for now as backend might need full impl
  Future<void> deleteTask(String id) async {
    // await _dio.delete('/tasks/$id');
  }
}

class Task {
  final String id;
  final String title;
  final String? status; // 'pending', 'completed'
  final String? priority;
  final String? contextNotes;
  final String? aiReasoning;

  Task({
    required this.id, 
    required this.title, 
    this.status, 
    this.priority,
    this.contextNotes,
    this.aiReasoning,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'].toString(),
      title: json['title'] ?? 'Untitled',
      status: json['status'],
      priority: json['priority'],
      contextNotes: json['context_notes'],
      aiReasoning: json['ai_reasoning'],
    );
  }
}

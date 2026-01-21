import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../../core/api/api_client.dart';
import 'package:dio/dio.dart';

part 'task_repository.g.dart';

@riverpod
TaskRepository taskRepository(TaskRepositoryRef ref) {
  return TaskRepository(ref.watch(apiClientProvider));
}

class TaskRepository {
  final Dio _dio;
  TaskRepository(this._dio);

  Future<int> getPendingTaskCount() async {
    final response = await _dio.get('/tasks');
    final tasks = response.data as List;
    return tasks.where((t) => !(t['completed'] ?? false)).length;
  }
}

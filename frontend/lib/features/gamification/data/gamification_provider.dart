import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../tasks/data/task_repository.dart';
import '../presentation/cloud_widget.dart';

part 'gamification_provider.g.dart';

@riverpod
Future<CloudState> cloudState(CloudStateRef ref) async {
  final repo = ref.watch(taskRepositoryProvider);
  
  try {
     final count = await repo.getPendingTaskCount();
     
     if (count == 0) return CloudState.clear;
     if (count > 5) return CloudState.storm;
     return CloudState.cloudy;
  } catch (e) {
    return CloudState.clear; // Default on error
  }
}

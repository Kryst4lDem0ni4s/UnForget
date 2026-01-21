import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/api/api_client.dart';

part 'ai_service.g.dart';

@riverpod
AiService aiService(AiServiceRef ref) {
  return AiService(ref.watch(apiClientProvider));
}

class AiService {
  final Dio _dio;

  AiService(this._dio);

  // Start the AI Pipeline
  Future<String> startAnalysis(String taskDescription, String userId) async {
    final response = await _dio.post('/ai/start', data: {
      'task_description': taskDescription,
      'user_id': userId, // In real app, from Auth Provider
    });
    return response.data['thread_id'];
  }

  // Check Status
  Future<Map<String, dynamic>> checkStatus(String threadId) async {
    final response = await _dio.get('/ai/$threadId/status');
    return response.data;
  }

  // Resume/Confirm Option
  Future<void> resumeWorkflow(String threadId, String selectedOptionId) async {
    await _dio.post('/ai/$threadId/resume', data: {
      'selected_option_id': selectedOptionId,
    });
  }
}

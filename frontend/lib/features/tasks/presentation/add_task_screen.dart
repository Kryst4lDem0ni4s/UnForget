import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../ai_assistant/data/ai_service.dart';

class AddTaskScreen extends ConsumerStatefulWidget {
  const AddTaskScreen({super.key});

  @override
  ConsumerState<AddTaskScreen> createState() => _AddTaskScreenState();
}

class _AddTaskScreenState extends ConsumerState<AddTaskScreen> {
  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  bool _isProcessing = false;

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    super.dispose();
  }

  Future<void> _startAiAnalysis() async {
    if (_titleController.text.isEmpty) return;

    setState(() => _isProcessing = true);
    
    // Simulate "Processing" quickly, real work is async backend
    try {
      final threadId = await ref.read(aiServiceProvider).startAnalysis(
        "${_titleController.text}\n${_descController.text}", 
        "user_1" // Mock User ID
      );
      
      if (mounted) {
        context.push('/plan-review/$threadId');
      }
    } catch (e) {
      if (mounted) {
         ScaffoldMessenger.of(context).showSnackBar(
           SnackBar(content: Text("Cloud Connection Error: $e")),
         );
      }
    } finally {
      if (mounted) {
        setState(() => _isProcessing = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add Task')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Task Title',
                hintText: 'e.g. Finish report',
                prefixIcon: Icon(Icons.check_circle_outline),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _descController,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Details / Context',
                hintText: 'e.g. Need 2 hours, high focus, before Friday.',
                alignLabelWithHint: true,
                prefixIcon: Icon(Icons.subject),
              ),
            ),
            const SizedBox(height: 24),
            
            // AI Info Card
            Card(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.cloud_sync, color: Theme.of(context).primaryColor),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('AI Auto-Scheduling', style: Theme.of(context).textTheme.titleSmall),
                          const SizedBox(height: 4),
                          const Text(
                            'SkyPlan will analyze your context and find the best time slots.',
                            style: TextStyle(fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _isProcessing ? null : _startAiAnalysis,
                icon: _isProcessing 
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) 
                    : const Icon(Icons.auto_awesome),
                label: Text(_isProcessing ? 'Analyzing Clouds...' : 'Analyze & Plan'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

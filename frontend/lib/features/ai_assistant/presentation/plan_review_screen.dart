import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:syncfusion_flutter_calendar/calendar.dart';
import '../../gamification/presentation/cloud_widget.dart';
import '../data/ai_service.dart';
import '../../calendar/presentation/smart_calendar.dart';

class PlanReviewScreen extends ConsumerStatefulWidget {
  final String threadId;
  const PlanReviewScreen({required this.threadId, super.key});

  @override
  ConsumerState<PlanReviewScreen> createState() => _PlanReviewScreenState();
}

class _PlanReviewScreenState extends ConsumerState<PlanReviewScreen> {
  Timer? _pollingTimer;
  Map<String, dynamic>? _analysisState;
  bool _isLoading = true;
  int _selectedOptionIndex = 0;
  final CalendarController _calendarController = CalendarController();

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  void _startPolling() {
    _pollingTimer = Timer.periodic(const Duration(seconds: 2), (timer) async {
      try {
        final status = await ref.read(aiServiceProvider).checkStatus(widget.threadId);
        final currentStatus = status['status'];
        
        if (currentStatus == 'human_review_required' || currentStatus == 'interrupted') {
           // We have options!
           timer.cancel();
           setState(() {
             _analysisState = status['state'];
             _isLoading = false;
           });
        }
      } catch (e) {
        // Handle error (retry or show error)
        print("Polling error: $e");
      }
    });
  }

  Future<void> _confirmPlan() async {
    final options = _analysisState?['scheduling_options'] as List;
    final selected = options[_selectedOptionIndex];
    // Need ID. If not present, use index (logic fallback)
    final optId = selected['id']?.toString() ?? (_selectedOptionIndex + 1).toString();
    
    await ref.read(aiServiceProvider).resumeWorkflow(widget.threadId, optId);
    
    if (mounted) {
      context.go('/'); // Back to Dashboard
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Plan Confirmed! Cloud updated.')),
      );
    }
  }

  List<Appointment> _getAppointments() {
    if (_isLoading || _analysisState == null) return [];
    
    final options = _analysisState!['scheduling_options'] as List;
    if (options.isEmpty) return [];

    final selected = options[_selectedOptionIndex];
    
    // Parse times
    // Backend format: "2026-01-22T10:00:00"
    final start = DateTime.parse(selected['start_time']);
    final end = DateTime.parse(selected['end_time']);
    
    // Focus calendar on this date
    // Note: Calling .displayDate in build can cause loops, but setting once is okay.
    // Ideally use controller.displayDate = start; in setState.
    
    return [
      Appointment(
        startTime: start,
        endTime: end,
        subject: "New Task (Proposed)",
        color: const Color(0xFF81D4FA), // Sky Blue
        isAllDay: false,
      ),
      // Mock existing block for context
      Appointment(
        startTime: start.subtract(const Duration(hours: 2)),
        endTime: start.subtract(const Duration(hours: 1)),
        subject: "Existing Meeting",
        color: Colors.grey,
      )
    ];
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const CloudWidget(state: CloudState.cloudy, size: 150),
              const SizedBox(height: 24),
              Text("The clouds are aligning...", style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 16),
              const CircularProgressIndicator(),
            ],
          ),
        ),
      );
    }

    final options = _analysisState?['scheduling_options'] as List? ?? [];

    return Scaffold(
      appBar: AppBar(title: const Text("Review Plan")),
      body: Column(
        children: [
          // 1. Suggestion Header
          Container(
             padding: const EdgeInsets.all(16),
             color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
             child: Row(
               children: [
                 const Icon(Icons.lightbulb_outline, color: Colors.orange),
                 const SizedBox(width: 8),
                 Expanded(
                   child: Text(
                     "I found ${options.length} options. This one minimizes travel time.", // Mock reasoning
                     style: Theme.of(context).textTheme.bodyMedium,
                   ),
                 ),
               ],
             ),
          ),
          
          // 2. Calendar View
          Expanded(
            child: SmartCalendar(
              appointments: _getAppointments(),
              controller: _calendarController,
            ),
          ),
          
          // 3. Option Selector (Carousel)
          Container(
            height: 180,
            padding: const EdgeInsets.symmetric(vertical: 16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10, offset: const Offset(0, -5))],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: Text("Select Option:", style: Theme.of(context).textTheme.titleSmall),
                ),
                const SizedBox(height: 8),
                Expanded(
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: options.length,
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    itemBuilder: (context, index) {
                      final opt = options[index];
                      final isSelected = index == _selectedOptionIndex;
                      final start = DateTime.parse(opt['start_time']);
                      
                      return GestureDetector(
                        onTap: () {
                           setState(() {
                             _selectedOptionIndex = index;
                           });
                           _calendarController.displayDate = start; 
                        },
                        child: Container(
                          width: 140,
                          margin: const EdgeInsets.only(right: 12),
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: isSelected ? Theme.of(context).colorScheme.primaryContainer : Colors.white,
                            border: Border.all(
                              color: isSelected ? Theme.of(context).colorScheme.primary : Colors.grey.shade300,
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                "Option ${index + 1}",
                                style: const TextStyle(fontWeight: FontWeight.bold),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                "${start.hour}:${start.minute.toString().padLeft(2, '0')}", // Simple format
                                style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontSize: 20),
                              ),
                              const SizedBox(height: 4),
                              Text("Score: ${opt['score'] ?? 'High'}", style: const TextStyle(fontSize: 10)),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _confirmPlan,
                      child: const Text("Confirm Schedule"),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

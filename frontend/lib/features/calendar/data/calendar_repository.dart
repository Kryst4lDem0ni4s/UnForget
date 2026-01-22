import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../../core/api/api_client.dart';

part 'calendar_repository.g.dart';

@riverpod
Future<List<CalendarEvent>> calendarEvents(CalendarEventsRef ref) async {
  final repo = ref.watch(calendarRepositoryProvider);
  return repo.getEvents();
}

@riverpod
CalendarRepository calendarRepository(CalendarRepositoryRef ref) {
  return CalendarRepository(ref.watch(apiClientProvider));
}

class CalendarRepository {
  final Dio _dio;
  CalendarRepository(this._dio);

  Future<List<CalendarEvent>> getEvents() async {
    try {
      final response = await _dio.get('/calendar/events');
      final List data = response.data;
      return data.map((json) => CalendarEvent.fromJson(json)).toList();
    } catch (e) {
      return []; // Return empty on error for MVP
    }
  }
}

class CalendarEvent {
  final String id;
  final String title;
  final DateTime start;
  final String? type;

  CalendarEvent({required this.id, required this.title, required this.start, this.type});

  factory CalendarEvent.fromJson(Map<String, dynamic> json) {
    return CalendarEvent(
      id: json['id'],
      title: json['title'],
      start: DateTime.parse(json['start']),
      type: json['type'],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:syncfusion_flutter_calendar/calendar.dart';
import '../data/calendar_repository.dart';

class CalendarScreen extends ConsumerWidget {
  const CalendarScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final eventsAsync = ref.watch(calendarEventsProvider);

    // Using Scaffold with transparent background and no AppBar to allow parent Shell title to show
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: eventsAsync.when(
        data: (events) {
          return SfCalendar(
            view: CalendarView.week,
            dataSource: _TaskDataSource(events),
            monthViewSettings: const MonthViewSettings(
              appointmentDisplayMode: MonthAppointmentDisplayMode.appointment,
            ),
            timeSlotViewSettings: const TimeSlotViewSettings(
              timeFormat: 'h:mm a',
            ),
            headerStyle: const CalendarHeaderStyle(
              textStyle: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error loading calendar: $err')),
      ),
    );
  }
}

class _TaskDataSource extends CalendarDataSource {
  _TaskDataSource(List<CalendarEvent> source) {
    appointments = source;
  }

  @override
  DateTime getStartTime(int index) {
    return _getEventData(index).start;
  }

  @override
  DateTime getEndTime(int index) {
    // Default to 1 hour duration if no end time (MVP)
    return _getEventData(index).start.add(const Duration(hours: 1));
  }

  @override
  String getSubject(int index) {
    return _getEventData(index).title;
  }

  @override
  Color getColor(int index) {
    return Colors.blueAccent; // Gamified blue
  }

  @override
  bool isAllDay(int index) {
    return false;
  }

  CalendarEvent _getEventData(int index) {
    final dynamic event = appointments![index];
    late final CalendarEvent calendarEvent;
    if (event is CalendarEvent) {
      calendarEvent = event;
    }
    
    return calendarEvent;
  }
}

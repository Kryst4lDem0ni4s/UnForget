import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_calendar/calendar.dart';

class SmartCalendar extends StatelessWidget {
  final List<Appointment> appointments;
  final CalendarController? controller;

  const SmartCalendar({
    super.key, 
    this.appointments = const [],
    this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return SfCalendar(
      view: CalendarView.week,
      controller: controller, // Allows programmatic navigation
      dataSource: Source(appointments),
      
      // Aesthetics ("Sleek")
      backgroundColor: Colors.white,
      cellBorderColor: Colors.transparent,
      selectionDecoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).primaryColor, width: 2),
        borderRadius: BorderRadius.circular(4),
      ),
      timeSlotViewSettings: const TimeSlotViewSettings(
        startHour: 7,
        endHour: 22,
        timeFormat: 'h a',
        timeIntervalHeight: 60,
      ),
      appointmentBuilder: (context, details) {
        final Appointment app = details.appointments.first;
        return Container(
          decoration: BoxDecoration(
             color: app.color.withOpacity(0.8),
             borderRadius: BorderRadius.circular(8),
             border: Border.all(color: app.color, width: 1),
          ),
          padding: const EdgeInsets.all(4),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                app.subject, 
                style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                maxLines: 1,
              ),
            ],
          ),
        );
      },
    );
  }
}

class Source extends CalendarDataSource {
  Source(List<Appointment> source) {
    appointments = source;
  }
}

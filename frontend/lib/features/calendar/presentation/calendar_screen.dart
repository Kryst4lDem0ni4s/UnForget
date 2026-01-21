import 'package:flutter/material.dart';
import 'simple_calendar_temp.dart'; 

class CalendarScreen extends StatelessWidget {
  const CalendarScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Schedule')),
      body: const SimpleCalendar(), 
    );
  }
}

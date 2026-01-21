import 'package:flutter/material.dart';

class SimpleCalendar extends StatelessWidget {
  const SimpleCalendar({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Month/Year header
        Container(
          padding: const EdgeInsets.all(16),
          color: Theme.of(context).primaryColor.withOpacity(0.1),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              IconButton(icon: const Icon(Icons.chevron_left), onPressed: () {}),
              Text(
                'January 2026',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              IconButton(icon: const Icon(Icons.chevron_right), onPressed: () {}),
            ],
          ),
        ),
        // Weekday headers
        Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                .map((day) => Expanded(
                      child: Center(
                        child: Text(
                          day,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ))
                .toList(),
          ),
        ),
        // Calendar grid (placeholder)
        Expanded(
          child: GridView.builder(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 7,
              childAspectRatio: 1,
            ),
            itemCount: 35,
            itemBuilder: (context, index) {
              final day = index + 1;
              return Container(
                margin: const EdgeInsets.all(2),
                decoration: BoxDecoration(
                  color: day == 15 ? Theme.of(context).primaryColor.withOpacity(0.2) : Colors.transparent,
                  border: Border.all(color: Colors.grey.shade300),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        '$day',
                        style: TextStyle(
                          fontWeight: day == 15 ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                      if (day == 15 || day == 20)
                        Container(
                          width: 4,
                          height: 4,
                          margin: const EdgeInsets.only(top: 2),
                          decoration: BoxDecoration(
                            color: Theme.of(context).primaryColor,
                            shape: BoxShape.circle,
                          ),
                        ),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

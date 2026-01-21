import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../tasks/data/task_repository.dart';
import 'widgets/adventurer_avatar.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Real Data Connection
    final tasksAsync = ref.watch(taskListProvider);
    
    // Gamification Logic
    final completedTasks = tasksAsync.valueOrNull?.where((t) => t.status == 'completed').length ?? 0;
    final totalTasks = tasksAsync.valueOrNull?.length ?? 0;
    
    final xp = completedTasks * 10;
    final level = (xp / 50).floor() + 1; // Level up every 50 XP (5 tasks)
    
    String title = "Novice Walker";
    if (level > 2) title = "Cloud Surfer";
    if (level > 5) title = "Sky Captain";

    return Scaffold(
      appBar: AppBar(
        title: const Text('ADVENTURER'),
      ),
      body: Center(
        child: Column(
          children: [
            const SizedBox(height: 40),
            // Character Card
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(32),
                border: Border.all(color: Colors.blue.shade100, width: 4),
                image: const DecorationImage(
                  image: AssetImage('assets/ui/pixel_ui_kit_tiles.png'),
                  opacity: 0.1,
                  repeat: ImageRepeat.repeat,
                ),
              ),
              child: Column(
                children: [
                   // Sliced Avatar based on Level (changes frame every 2 levels)
                  SlicedSprite(
                    frameIndex: level % 4, // Cycle through 4 frames
                    totalFrames: 4,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    title,
                    style: GoogleFonts.pressStart2p(fontSize: 14), // Smaller to fit
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "Level $level Planner",
                    style: GoogleFonts.outfit(fontSize: 16, color: Colors.grey),
                  ),
                  const SizedBox(height: 12),
                  // XP Bar
                  SizedBox(
                    width: 150,
                    child: LinearProgressIndicator(
                      value: (xp % 50) / 50, // Progress to next level
                      backgroundColor: Colors.grey.shade200,
                      color: Colors.orange,
                      minHeight: 8,
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text("${xp % 50} / 50 XP", style: const TextStyle(fontSize: 10, color: Colors.grey))
                ],
              ),
            ),
            const SizedBox(height: 32),
            // Stats Row
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _StatTile(label: "TOTAL XP", value: "$xp", color: Colors.purple),
                  _StatTile(label: "LOG", value: "$completedTasks/$totalTasks", color: Colors.orange),
                  _StatTile(label: "RANK", value: "$level", color: Colors.blue),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StatTile extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _StatTile({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: GoogleFonts.pressStart2p(fontSize: 8, color: color),
        ),
        const SizedBox(height: 8),
        Text(
          value,
          style: GoogleFonts.outfit(fontSize: 20, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}

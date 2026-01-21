import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
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
                  Image.asset(
                    'assets/ui/pixel_character_kit.png',
                    width: 150,
                    height: 150,
                    fit: BoxFit.contain,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "CLOUD WALKER",
                    style: GoogleFonts.pressStart2p(fontSize: 18),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "Level 5 Planner",
                    style: GoogleFonts.outfit(fontSize: 16, color: Colors.grey),
                  ),
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
                  _StatTile(label: "XP", value: "1,250", color: Colors.purple),
                  _StatTile(label: "STREAK", value: "7 Days", color: Colors.orange),
                  _StatTile(label: "TASKS", value: "42", color: Colors.blue),
                ],
              ),
            ),
            const Spacer(),
            // Loot / Equipment Grid (Visual Only)
            Text(
              "INVENTORY",
              style: GoogleFonts.pressStart2p(fontSize: 12),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 100,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 24),
                itemCount: 5,
                itemBuilder: (context, index) {
                  return Container(
                    width: 60,
                    margin: const EdgeInsets.only(right: 12),
                    decoration: BoxDecoration(
                      color: Colors.grey.shade100,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.grey.shade300),
                    ),
                    child: Icon(Icons.cloud_outlined, color: Colors.grey.shade400),
                  );
                },
              ),
            ),
            const SizedBox(height: 40),
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

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';

class SyncVisualizer extends StatelessWidget {
  final bool isSyncing;

  const SyncVisualizer({super.key, required this.isSyncing});

  @override
  Widget build(BuildContext context) {
    if (!isSyncing) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: Colors.blue.shade100, width: 2),
        boxShadow: [
          BoxShadow(
            color: Colors.blue.withOpacity(0.1),
            blurRadius: 10,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Image.asset(
            'assets/ui/pixel_sync_animation.png',
            width: 24,
            height: 24,
          ).animate(onPlay: (controller) => controller.repeat())
           .rotate(duration: 2.seconds),
          const SizedBox(width: 12),
          Text(
            "SYNCING DATA...",
            style: GoogleFonts.pressStart2p(
              fontSize: 8,
              color: Colors.blue.shade700,
            ),
          ),
        ],
      ),
    ).animate().fadeIn().slideY(begin: 1.0, end: 0.0);
  }
}

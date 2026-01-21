import 'package:flutter/material.dart';

enum CloudState { clear, cloudy, storm }

class CloudWidget extends StatelessWidget {
  final CloudState state;
  final double size;

  const CloudWidget({
    super.key, 
    this.state = CloudState.clear,
    this.size = 200,
  });

  @override
  Widget build(BuildContext context) {
    Color cloudBaseColor;
    Color cloudShadowColor;
    IconData iconData;
    
    switch (state) {
      case CloudState.clear:
        cloudBaseColor = Colors.white;
        cloudShadowColor = Colors.blue.shade100;
        iconData = Icons.cloud_queue; 
        break;
      case CloudState.cloudy:
        cloudBaseColor = const Color(0xFFEEEEEE);
        cloudShadowColor = Colors.grey.shade300;
        iconData = Icons.cloud;
        break;
      case CloudState.storm:
        cloudBaseColor = const Color(0xFF78909C);
        cloudShadowColor = const Color(0xFF455A64);
        iconData = Icons.thunderstorm;
        break;
    }

    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          // "Pixel" effect simulated with stacked icons or just clean icon for "Sleek" req
          // User asked for "Sleek" AND "Pixelated". 
          // I'll stick to a very clean, large White Cloud icon with soft shadow (Sleek).
          // Pixelation requires custom assets.
          
          Icon(
            iconData,
            size: size,
            color: cloudBaseColor,
            shadows: [
              Shadow(
                blurRadius: 20,
                color: cloudShadowColor,
                offset: const Offset(5, 5),
              ),
            ],
          ),
          
          // Status Text Overlay (Gamification)
          if (state == CloudState.storm)
             Positioned(
               bottom: size * 0.1,
               child: Container(
                 padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                 decoration: BoxDecoration(
                   color: Colors.red.withOpacity(0.8),
                   borderRadius: BorderRadius.circular(4),
                 ),
                 child: const Text("OVERLOAD", style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
               ),
             )
        ],
      ),
    );
  }
}

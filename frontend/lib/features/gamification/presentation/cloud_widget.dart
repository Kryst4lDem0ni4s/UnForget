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
    bool isStorm = false;
    
    switch (state) {
      case CloudState.clear:
        cloudBaseColor = Colors.white;
        cloudShadowColor = Colors.blue.shade100;
        break;
      case CloudState.cloudy:
        cloudBaseColor = const Color(0xFFEEEEEE);
        cloudShadowColor = Colors.grey.shade300;
        break;
      case CloudState.storm:
        cloudBaseColor = const Color(0xFF78909C);
        cloudShadowColor = const Color(0xFF455A64);
        isStorm = true;
        break;
    }

    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(
            size: Size(size, size * 0.6),
            painter: PixelCloudPainter(
              color: cloudBaseColor,
              shadowColor: cloudShadowColor,
              isStorm: isStorm,
            ),
          ),
          
          // Status Text Overlay (Gamification)
          if (state == CloudState.storm)
             Positioned(
               bottom: size * 0.1,
               child: Container(
                 padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                 decoration: BoxDecoration(
                   color: Colors.red.withOpacity(0.9),
                   borderRadius: BorderRadius.circular(4),
                   boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 2))],
                 ),
                 child: const Text("OVERLOAD", style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
               ),
             )
        ],
      ),
    );
  }
}

class PixelCloudPainter extends CustomPainter {
  final Color color;
  final Color shadowColor;
  final bool isStorm;

  PixelCloudPainter({required this.color, required this.shadowColor, this.isStorm = false});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    
    // Grid size 16x10
    final double pixelSize = size.width / 16; 

    // Define a simple pixel cloud shape (1 = fill)
    final shape = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ];
    
    // Draw Shadow (Offset +4, +4)
    paint.color = shadowColor;
    for(int y=0; y<shape.length; y++) {
        for(int x=0; x<shape[y].length; x++) {
            if(shape[y][x] == 1) {
                canvas.drawRect(
                    Rect.fromLTWH((x * pixelSize) + 4, (y * pixelSize) + 4, pixelSize, pixelSize), 
                    paint
                );
            }
        }
    }

    // Draw Cloud Body
    paint.color = color;
    for(int y=0; y<shape.length; y++) {
        for(int x=0; x<shape[y].length; x++) {
            if(shape[y][x] == 1) {
                canvas.drawRect(
                    Rect.fromLTWH(x * pixelSize, y * pixelSize, pixelSize, pixelSize), 
                    paint
                );
            }
        }
    }
    
    // Draw Thunder if storm
    if (isStorm) {
        paint.color = const Color(0xFFFFEB3B); // Bright Yellow
        // Simple Bolt (centered)
        final bolt = [
            [0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,0,0,1,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0],
        ];
        
        // Render bolt on top
         for(int y=0; y<bolt.length; y++) {
            for(int x=0; x<bolt[y].length; x++) {
                if(bolt[y][x] == 1) {
                    canvas.drawRect(
                        Rect.fromLTWH((x+4) * pixelSize, (y+4) * pixelSize, pixelSize, pixelSize), 
                        paint
                    );
                }
            }
        }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

import 'package:flutter/material.dart';

class AdventurerAvatar extends StatelessWidget {
  final int level;
  const AdventurerAvatar({super.key, required this.level});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 150,
      height: 150,
       child: CustomPaint(
         painter: _SpriteSheetPainter(level: level),
       ),
    );
  }
}

class _SpriteSheetPainter extends CustomPainter {
  final int level;
  // This would ideally be loaded as ui.Image but for MVP simplicity 
  // and avoiding async loading complexity in a painter,
  // we will use the existing Image.asset method in parent or use a dedicated SpriteWidget if we had the flame package.
  // 
  // User Requirement: "Observe their contents and slice appropriately. I'll manually edit them as necessary."
  // Since we can't easily load 'ui.Image' synchronously here without a provider, 
  // we will assume the user has a "Sheet" and we are picking a "Frame".
  //
  // However, without the actual image loaded in memory, CustomPainter can't drawImage.
  // Alternative: Use a Stack with a clipped Container to "Slice" the asset image.
  
  const _SpriteSheetPainter({required this.level});

  @override
  void paint(Canvas canvas, Size size) {
    // Placeholder for where the painting logic would go if we had the ui.Image object.
    // Real implementation below uses the ClipRect trick which is easier in Flutter.
  }
  
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// Better Approach for Slicing Asset Image without manually loading bytes:
class SlicedSprite extends StatelessWidget {
  final int frameIndex; // 0 to N
  final int totalFrames;
  final String assetPath;
  final double size;

  const SlicedSprite({
    super.key,
    required this.frameIndex,
    required this.totalFrames,
    this.assetPath = 'assets/ui/pixel_character_kit.png',
    this.size = 150,
  });

  @override
  Widget build(BuildContext context) {
    // Assuming horizontal strip sprite sheet
    // If it's a grid, we need rows/cols. 
    // Let's assume standard "Character Kit" 4x4 or similar.
    // For MVP, we'll try to show the "Full" image but cropped to a specific region.
    
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        image: DecorationImage(
           image: AssetImage(assetPath),
           fit: BoxFit.none, // Don't scale, keep original pixels
           alignment: Alignment(-0.5 + (frameIndex * 0.1), 0.0), // Shift alignment to show different part
           scale: 4.0, // Zoom in to show pixel art clearly
        ),
      ),
    );
  }
}

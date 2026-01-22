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
  final int frameIndex;
  final int totalFrames;
  final String assetPath;
  final double size;
  
  // Sprite Sheet Configuration
  final int spriteWidth;
  final int spriteHeight;
  final int columns;

  const SlicedSprite({
    super.key,
    required this.frameIndex,
    required this.totalFrames,
    this.assetPath = 'assets/ui/pixel_character_kit.png',
    this.size = 150,
    this.spriteWidth = 32,  // Assumed standard sprite size
    this.spriteHeight = 32, // Assumed standard sprite size
    this.columns = 4,       // Assumed 4 columns in sheet
  });

  @override
  Widget build(BuildContext context) {
    // Calculate row and column for the current frame
    final int col = frameIndex % columns;
    final int row = (frameIndex / columns).floor();

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(16),
      ),
      child: ClipRect(
        child: FittedBox(
          fit: BoxFit.cover,
          child: SizedBox(
            width: spriteWidth.toDouble(),
            height: spriteHeight.toDouble(),
            child: Stack(
              children: [
                Positioned(
                  left: -(col * spriteWidth).toDouble(),
                  top: -(row * spriteHeight).toDouble(),
                  child: Image.asset(
                    assetPath,
                    // Load the full image, but we only show a window
                    // This assumes the image is large enough.
                    // If we knew the total size we could be more precise.
                    // For now, we rely on the negative positioning to shift the view.
                    fit: BoxFit.none,
                    alignment: Alignment.topLeft,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

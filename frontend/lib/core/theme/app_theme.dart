import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Brand Colors - "Cloudy Sky"
  static const Color skyBlueLight = Color(0xFFE1F5FE); // Very light blue background
  static const Color skyBlue = Color(0xFF81D4FA);      // Primary Brand Color
  static const Color stormGrey = Color(0xFF607D8B);    // Accent / Stormy
  static const Color sweetWhite = Color(0xFFFFFFFF);
  static const Color charcoal = Color(0xFF37474F);     // Text color (Blue-ish dark grey)
  
  static TextTheme _buildTextTheme() {
    return GoogleFonts.outfitTextTheme().copyWith(
      displayLarge: GoogleFonts.pressStart2p(color: charcoal),
      displayMedium: GoogleFonts.pressStart2p(color: charcoal),
      displaySmall: GoogleFonts.pressStart2p(color: charcoal),
      headlineLarge: GoogleFonts.pressStart2p(color: charcoal),
      headlineMedium: GoogleFonts.pressStart2p(color: charcoal),
      headlineSmall: GoogleFonts.pressStart2p(color: charcoal),
    ).apply(
      displayColor: charcoal,
      bodyColor: charcoal,
    );
  }

  static ThemeData light() {
    return ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: skyBlueLight,
      colorScheme: ColorScheme.fromSeed(
        seedColor: skyBlue,
        primary: skyBlue,
        secondary: stormGrey,
        surface: sweetWhite,
        error: const Color(0xFFEF5350),
      ),
      textTheme: _buildTextTheme(),
      
      // AppBar
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(color: charcoal, fontSize: 20, fontWeight: FontWeight.bold),
        iconTheme: IconThemeData(color: charcoal),
      ),
      
      // Buttons
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: skyBlue,
          foregroundColor: charcoal, // Dark text on light blue looks playful
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)), // Cloud-like rounding
          textStyle: GoogleFonts.outfit(fontWeight: FontWeight.bold, fontSize: 16),
        ),
      ),
      
      // Cards - Floating Look
      cardTheme: CardTheme(
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        color: Colors.white.withOpacity(0.8), // Glassy cloud
        margin: const EdgeInsets.all(8),
      ),
      
      // Inputs
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(20),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(20),
          borderSide: const BorderSide(color: Colors.white),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(20),
          borderSide: const BorderSide(color: skyBlue, width: 2),
        ),
        contentPadding: const EdgeInsets.all(20),
      ),
      
      // Navigation Bar
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white.withOpacity(0.9),
        indicatorColor: skyBlue.withOpacity(0.5),
        labelTextStyle: WidgetStateProperty.all(
          const TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: charcoal),
        ),
      ),
    );
  }
}

import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'streak_repository.g.dart';

@riverpod
StreakRepository streakRepository(StreakRepositoryRef ref) {
  throw UnimplementedError('Initialize with override');
}

@riverpod
Future<int> currentStreak(CurrentStreakRef ref) async {
  final repo = ref.watch(streakRepositoryProvider);
  await repo.updateStreak();
  return repo.getStreak();
}

class StreakRepository {
  final SharedPreferences _prefs;
  static const String _lastLoginKey = 'last_login_date';
  static const String _streakKey = 'current_streak';

  StreakRepository(this._prefs);

  int getStreak() {
    return _prefs.getInt(_streakKey) ?? 0;
  }

  Future<void> updateStreak() async {
    final lastLoginStr = _prefs.getString(_lastLoginKey);
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);

    if (lastLoginStr == null) {
      // First login ever
      await _prefs.setString(_lastLoginKey, today.toIso8601String());
      await _prefs.setInt(_streakKey, 1);
      return;
    }

    final lastLoginDate = DateTime.parse(lastLoginStr);
    final difference = today.difference(lastLoginDate).inDays;

    if (difference == 0) {
      // Already logged in today, do nothing
      return;
    } else if (difference == 1) {
      // Consecutive day
      final current = getStreak();
      await _prefs.setInt(_streakKey, current + 1);
    } else {
      // Streak broken
      await _prefs.setInt(_streakKey, 1);
    }
    
    await _prefs.setString(_lastLoginKey, today.toIso8601String());
  }
}

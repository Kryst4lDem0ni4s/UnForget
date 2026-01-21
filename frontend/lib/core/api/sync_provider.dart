import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'sync_provider.g.dart';

@riverpod
class SyncStatus extends _$SyncStatus {
  @override
  bool build() => false;

  void startSync() => state = true;
  void endSync() => state = false;
}

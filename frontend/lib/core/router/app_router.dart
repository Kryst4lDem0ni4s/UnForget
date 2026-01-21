import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/tasks/presentation/add_task_screen.dart';
import '../../features/tasks/presentation/task_list_screen.dart';
import '../../features/calendar/presentation/calendar_screen.dart';
import '../../features/ai_assistant/presentation/plan_review_screen.dart';

part 'app_router.g.dart';

@riverpod
GoRouter router(RouterRef ref) {
  return GoRouter(
    initialLocation: '/', // TODO: Change to /login based on auth state
    debugLogDiagnostics: true,
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const DashboardScreen(),
        routes: [
          GoRoute(
            path: 'add-task',
            builder: (context, state) => const AddTaskScreen(),
          ),
        ],
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/plan-review/:threadId',
        builder: (context, state) {
          final threadId = state.pathParameters['threadId']!;
          return PlanReviewScreen(threadId: threadId);
        },
      ),
      GoRoute(
        path: '/calendar',
        builder: (context, state) => const CalendarScreen(),
      ),
      GoRoute(
        path: '/tasks',
        builder: (context, state) => const TaskListScreen(),
      ),
    ],
  );
}

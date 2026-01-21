import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
AUTH_HEADERS = {"Authorization": "Bearer test-user"}

print("=" * 80)
print("AI PLANNER BACKEND - COMPREHENSIVE STRESS TEST")
print("=" * 80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Track results
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_endpoint(name, method, url, expected_status, **kwargs):
    """Helper to test an endpoint."""
    try:
        print(f"\n📍 Testing: {name}")
        print(f"   URL: {method} {url}")
        
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        elapsed = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == expected_status:
            print(f"   ✅ PASSED (Status: {response.status_code}, Time: {elapsed:.2f}ms)")
            test_results["passed"] += 1
            return response
        else:
            print(f"   ❌ FAILED (Expected: {expected_status}, Got: {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            test_results["failed"] += 1
            test_results["errors"].append(f"{name}: Status mismatch")
            return None
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"{name}: {str(e)}")
        return None

# TEST SUITE
print("\n\n PHASE 1: BASIC ENDPOINTS")
print("-" * 80)

# Test 1: Root endpoint
test_endpoint(
    "Root Endpoint",
    "GET",
    f"{BASE_URL}/",
    200
)
 
# Test 2: Health check
test_endpoint(
    "Health Check",
    "GET",
    f"{BASE_URL}/health",
    200
)

# Test 3: Get current user
test_endpoint(
    "Get Current User",
    "GET",
    f"{BASE_URL}/api/v1/users/me",
    200,
    headers=AUTH_HEADERS
)

print("\n\n PHASE 2: TASK MANAGEMENT")
print("-" * 80)

# Test 4: Create task
task_response = test_endpoint(
    "Create Task",
    "POST",
    f"{BASE_URL}/api/v1/tasks/",
    200,
    headers=AUTH_HEADERS,
    json={
        "title": "Stress Test Task",
        "description": "This is a comprehensive test task",
        "priority": "high",
        "context_notes": "Testing the AI pipeline"
    }
)

task_id = None
if task_response:
    task_data = task_response.json()
    task_id = task_data.get("id")
    print(f"   📝 Created Task ID: {task_id}")

# Test 5: List tasks
test_endpoint(
    "List Tasks",
    "GET",
    f"{BASE_URL}/api/v1/tasks/",
    200,
    headers=AUTH_HEADERS
)

# Test 6: Get specific task
if task_id:
    test_endpoint(
        "Get Task by ID",
        "GET",
        f"{BASE_URL}/api/v1/tasks/{task_id}",
        200,
        headers=AUTH_HEADERS
    )

print("\n\n PHASE 3: AI PIPELINE TESTING")
print("-" * 80)

if task_id:
    # Test 7: AI Task Analysis
    analyze_response = test_endpoint(
        "AI Task Analysis",
        "POST",
        f"{BASE_URL}/api/v1/ai/analyze-task",
        200,
        headers=AUTH_HEADERS,
        json={"task_id": task_id}
    )
    
    if analyze_response:
        analysis = analyze_response.json()
        print(f"   🤖 AI Analysis Results:")
        print(f"      - Estimated Duration: {analysis.get('estimated_duration_minutes')} minutes")
        print(f"      - Suggested Tags: {analysis.get('suggested_tags')}")
        print(f"      - Reasoning: {analysis.get('ai_reasoning')}")
    
    # Test 8: AI Scheduling
    schedule_response = test_endpoint(
        "AI Scheduling",
        "POST",
        f"{BASE_URL}/api/v1/ai/schedule",
        200,
        headers=AUTH_HEADERS,
        json={"task_id": task_id}
    )
    
    if schedule_response:
        schedule = schedule_response.json()
        print(f"   📅 Scheduling Options:")
        for i, option in enumerate(schedule.get('options', []), 1):
            print(f"      Option {i}:")
            print(f"         Start: {option.get('start_time')}")
            print(f"         End: {option.get('end_time')}")
            print(f"         Reasoning: {option.get('reasoning')}")
else:
    print("   ⚠️ Skipping AI tests (no task created)")

print("\n\n PHASE 4: CALENDAR SYNC TESTING")
print("-" * 80)

# Test 9: Google Calendar Sync
test_endpoint(
    "Google Calendar Sync",
    "POST",
    f"{BASE_URL}/api/v1/calendar/sync",
    200,
    headers=AUTH_HEADERS,
    json={"provider": "google"}
)

# Test 10: Microsoft Calendar Sync
test_endpoint(
    "Microsoft Calendar Sync",
    "POST",
    f"{BASE_URL}/api/v1/calendar/sync",
    200,
    headers=AUTH_HEADERS,
    json={"provider": "microsoft"}
)

# Test 11: List Calendar Events
test_endpoint(
    "List Calendar Events",
    "GET",
    f"{BASE_URL}/api/v1/calendar/events",
    200,
    headers=AUTH_HEADERS
)

# Test 12: Invalid Provider (Should fail)
test_endpoint(
    "Invalid Calendar Provider",
    "POST",
    f"{BASE_URL}/api/v1/calendar/sync",
    400,  # Should return 400 Bad Request
    headers=AUTH_HEADERS,
    json={"provider": "invalid"}
)

print("\n\n PHASE 5: ERROR HANDLING")
print("-" * 80)

# Test 13: Non-existent task
test_endpoint(
    "Non-existent Task",
    "POST",
    f"{BASE_URL}/api/v1/ai/analyze-task",
    404,
    headers=AUTH_HEADERS,
    json={"task_id": "00000000-0000-0000-0000-999999999999"}
)

# Test 14: Unauthorized access (no auth header)
test_endpoint(
    "Unauthorized Access",
    "GET",
    f"{BASE_URL}/api/v1/tasks/",
    403  # Should be forbidden
)

# Test 15: Invalid auth token
test_endpoint(
    "Invalid Auth Token",
    "GET",
    f"{BASE_URL}/api/v1/users/me",
    401,  # Unauthorized
    headers={"Authorization": "Bearer invalid-token"}
)

# FINAL SUMMARY
print("\n\n" + "=" * 80)
print("STRESS TEST SUMMARY")
print("=" * 80)
print(f"✅ Tests Passed: {test_results['passed']}")
print(f"❌ Tests Failed: {test_results['failed']}")
print(f"📊 Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")
print(f"⏱️ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if test_results['errors']:
    print(f"\n❌ Errors:")
    for error in test_results['errors']:
        print(f"   - {error}")

print("\n" + "=" * 80)

# Exit with appropriate code
exit(0 if test_results['failed'] == 0 else 1)

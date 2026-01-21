import requests
import json

BASE_URL = "http://localhost:8000"
AUTH_HEADERS = {"Authorization": "Bearer test-user"}

print("=" * 60)
print("AI Planner Backend API Test")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Health check
print("\n2. Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 3: Get current user
print("\n3. Testing get current user...")
response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=AUTH_HEADERS)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 4: Create a task
print("\n4. Testing task creation...")
task_data = {
    "title": "Complete Backend Testing",
    "description": "Verify all API endpoints",
    "priority": "high",
    "context_notes": "This is a comprehensive test"
}
response = requests.post(
    f"{BASE_URL}/api/v1/tasks/",
    headers=AUTH_HEADERS,
    json=task_data
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    task = response.json()
    print(f"Created Task ID: {task['id']}")
    print(f"Task Title: {task['title']}")
    print(f"Task Status: {task['status']}")
    task_id = task['id']
else:
    print(f"Error: {response.text}")
    task_id = None

# Test 5: List tasks
print("\n5. Testing list tasks...")
response = requests.get(f"{BASE_URL}/api/v1/tasks/", headers=AUTH_HEADERS)
print(f"Status: {response.status_code}")
tasks = response.json()
print(f"Total tasks: {len(tasks)}")
for task in tasks:
    print(f"  - {task['title']} (Status: {task['status']})")

# Test 6: Get specific task
if task_id:
    print(f"\n6. Testing get task by ID: {task_id}...")
    response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}", headers=AUTH_HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)

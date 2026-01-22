import requests

# Test the full flow
print("1. Testing login...")
login_response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/login",
    json={"email": "test@example.com", "password": "test123"}
)
print(f"   Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"   Token: {token[:50]}...")
    
    print("\n2. Testing task creation with token...")
    task_response = requests.post(
        "http://127.0.0.1:8000/api/v1/tasks/",
        json={"title": "Test Task", "priority": "high"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"   Status: {task_response.status_code}")
    print(f"   Response: {task_response.text[:200]}")
else:
    print(f"   Login failed: {login_response.text}")

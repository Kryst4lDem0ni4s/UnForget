import requests
import json

BASE_URL = "http://localhost:8000"
headers = {"Authorization": "Bearer test-user"}

try:
    # 1. Create Task
    print("Creating task...")
    res = requests.post(f"{BASE_URL}/api/v1/tasks/", json={"title": "Test AI", "priority": "high"}, headers=headers)
    print(f"Create Status: {res.status_code}")
    if res.status_code != 200:
        print(res.text)
        exit(1)
    
    task_id = res.json()["id"]
    print(f"Task ID: {task_id}")
    
    # 2. Call AI Analyze
    print("Calling Analyze...")
    res = requests.post(f"{BASE_URL}/api/v1/ai/analyze-task", json={"task_id": task_id}, headers=headers)
    print(f"Analyze Status: {res.status_code}")
    print(res.text)

except Exception as e:
    print(f"Error: {e}")

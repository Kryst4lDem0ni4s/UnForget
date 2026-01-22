import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_auth_flow():
    print("1. Login...")
    try:
        login_resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
            timeout=5
        )
        print(f"Login Status: {login_resp.status_code}")
        if login_resp.status_code != 200:
            print(f"Login Failed: {login_resp.text}")
            return

        token = login_resp.json()["access_token"]
        print("Login Success. Token received.")
        
        print("\n2. Create Task with Token...")
        headers = {"Authorization": f"Bearer {token}"}
        task_data = {
            "title": "Test Task via Script",
            "priority": "high"
        }
        task_resp = requests.post(
            f"{BASE_URL}/tasks/",
            json=task_data,
            headers=headers,
            timeout=5
        )
        print(f"Task Create Status: {task_resp.status_code}")
        if task_resp.status_code == 200:
            print("Task Created Successfully!")
            print(f"Task: {task_resp.json()}")
        else:
            print(f"Task Create Failed: {task_resp.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth_flow()

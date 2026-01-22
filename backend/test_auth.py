import requests
import json

url = "http://127.0.0.1:8000/api/v1/auth/login"
data = {"email": "test@example.com", "password": "testpass123"}

print(f"Testing POST {url}")
print(f"Data: {json.dumps(data, indent=2)}")

response = requests.post(url, json=data)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

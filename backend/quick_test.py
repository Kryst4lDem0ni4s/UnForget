import requests

print("Quick Server Health Check")
print("=" * 40)

try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Server is running")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("❌ Server is not running")
    print("   Please start the server with: uvicorn app.main:app --reload")
except Exception as e:
    print(f"❌ Error: {e}")

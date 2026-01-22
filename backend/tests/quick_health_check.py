"""
Quick health check for the backend API
"""
import requests
import sys

def test_basic_connectivity():
    """Test if backend is reachable at all"""
    print("Testing basic connectivity to http://127.0.0.1:8000")
    
    try:
        # Try the root endpoint with a short timeout
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        print(f" Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        print(" Connection timed out - server may be hanging")
        return False
    except requests.exceptions.ConnectionError:
        print(" Connection refused - server may not be running")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\nTesting health endpoint")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        print(f" Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        print(" Health check timed out")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Backend Quick Health Check")
    print("=" * 60)
    
    if not test_basic_connectivity():
        print("\n⚠️  Backend server appears to be stuck or not running")
        print("   Try restarting the uvicorn server")
        sys.exit(1)
    
    if not test_health():
        print("\n⚠️  Health endpoint not responding")
        sys.exit(1)
    
    print("\n Backend is responding correctly!")
    sys.exit(0)

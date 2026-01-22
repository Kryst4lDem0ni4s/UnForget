"""
Integration Test Suite for AI Planner Backend API

Tests the complete lifecycle of:
- Health checks
- Task CRUD operations
- Calendar integration
- AI endpoints

Run this with: python tests/integration_suite.py
"""

import requests
import sys
from datetime import datetime, timedelta
from typing import Optional

BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Test user credentials (ensure you have a test user or use auth bypass for testing)
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpass123"


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class IntegrationTestSuite:
    def __init__(self):
        self.auth_token: Optional[str] = None
        self.created_task_id: Optional[str] = None
        self.passed = 0
        self.failed = 0
        
    def log_test(self, test_name: str):
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST]{Colors.RESET} {test_name}")
    
    def log_success(self, message: str):
        self.passed += 1
        print(f"  {Colors.GREEN}[PASS]{Colors.RESET} {message}")
    
    def log_failure(self, message: str):
        self.failed += 1
        print(f"  {Colors.RED}[FAIL]{Colors.RESET} {message}")
    
    def log_info(self, message: str):
        print(f"  {Colors.YELLOW}[INFO]{Colors.RESET} {message}")
    
    def test_health_check(self):
        """Test 1: Health endpoint"""
        self.log_test("Health Check")
        
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            
            if response.status_code == 200:
                self.log_success(f"Health endpoint returned 200")
                
                data = response.json()
                if data.get("status") == "ok":
                    self.log_success(f"Status is 'ok': {data}")
                else:
                    self.log_failure(f"Unexpected status: {data}")
            else:
                self.log_failure(f"Health check failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Health check exception: {e}")
            sys.exit(1)
    
    def test_root_endpoint(self):
        """Test 2: Root endpoint"""
        self.log_test("Root Endpoint")
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            
            if response.status_code == 200:
                self.log_success(f"Root endpoint returned 200")
                data = response.json()
                self.log_info(f"Message: {data.get('message')}")
            else:
                self.log_failure(f"Root endpoint failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Root endpoint exception: {e}")
    
    def test_authentication(self):
        """Test 3: Authentication (if enabled)"""
        self.log_test("Authentication")
        
        try:
            # Try to login test user - use JSON format with email/password
            login_response = requests.post(
                f"{API_V1}/auth/login",
                json={
                    "email": TEST_USER_EMAIL,
                    "password": TEST_USER_PASSWORD
                },
                timeout=5
            )
            
            if login_response.status_code == 200:
                data = login_response.json()
                self.auth_token = data.get("access_token")
                self.log_success(f"Login successful, got token")
            elif login_response.status_code == 401:
                # Try to register
                self.log_info("User not found, attempting registration...")
                register_response = requests.post(
                    f"{API_V1}/auth/register",
                    json={
                        "email": TEST_USER_EMAIL,
                        "password": TEST_USER_PASSWORD,
                        "full_name": "Test User"
                    },
                    timeout=5
                )
                
                if register_response.status_code in [200, 201]:
                    self.log_success("Registration successful")
                    # Try login again
                    login_response = requests.post(
                        f"{API_V1}/auth/login",
                        json={
                            "email": TEST_USER_EMAIL,
                            "password": TEST_USER_PASSWORD
                        },
                        timeout=5
                    )
                    if login_response.status_code == 200:
                        data = login_response.json()
                        self.auth_token = data.get("access_token")
                        self.log_success(f"Login after registration successful")
                else:
                    self.log_failure(f"Registration failed: {register_response.status_code}")
            else:
                self.log_failure(f"Login failed with unexpected status: {login_response.status_code}")
                
        except Exception as e:
            self.log_info(f"Auth not configured or error: {e}")
            self.log_info("Continuing tests without authentication...")
    
    def get_headers(self):
        """Get headers with auth token if available"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    def test_create_task(self):
        """Test 4: Create a new task"""
        self.log_test("Create Task")
        
        try:
            task_data = {
                "title": "Integration Test Task",
                "description": "This is a test task created by integration suite",
                "priority": "high",
                "status": "pending",
                "deadline": (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            response = requests.post(
                f"{API_V1}/tasks/",
                json=task_data,
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.created_task_id = str(data.get("id"))
                self.log_success(f"Task created with ID: {self.created_task_id}")
                self.log_info(f"Task title: {data.get('title')}")
            else:
                self.log_failure(f"Create task failed with status {response.status_code}")
                self.log_info(f"Response: {response.text}")
                
        except Exception as e:
            self.log_failure(f"Create task exception: {e}")
    
    def test_get_tasks(self):
        """Test 5: Retrieve all tasks"""
        self.log_test("Get Tasks")
        
        try:
            response = requests.get(
                f"{API_V1}/tasks/",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"Retrieved {len(data)} task(s)")
                
                # Verify our created task is in the list
                if self.created_task_id:
                    task_ids = [str(t.get("id")) for t in data]
                    if self.created_task_id in task_ids:
                        self.log_success(f"Created task found in list")
                    else:
                        self.log_failure(f"Created task NOT found in list")
            else:
                self.log_failure(f"Get tasks failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Get tasks exception: {e}")
    
    def test_get_single_task(self):
        """Test 6: Get a specific task by ID"""
        self.log_test("Get Single Task")
        
        if not self.created_task_id:
            self.log_info("Skipping - no task ID available")
            return
        
        try:
            response = requests.get(
                f"{API_V1}/tasks/{self.created_task_id}",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"Retrieved task: {data.get('title')}")
                self.log_info(f"Status: {data.get('status')}, Priority: {data.get('priority')}")
            else:
                self.log_failure(f"Get single task failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Get single task exception: {e}")
    
    def test_update_task(self):
        """Test 7: Update a task"""
        self.log_test("Update Task")
        
        if not self.created_task_id:
            self.log_info("Skipping - no task ID available")
            return
        
        try:
            update_data = {
                "status": "completed",
                "priority": "medium"
            }
            
            response = requests.put(
                f"{API_V1}/tasks/{self.created_task_id}",
                json=update_data,
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"Task updated")
                
                # Verify the update
                if data.get("status") == "completed":
                    self.log_success(f"Status changed to 'completed'")
                else:
                    self.log_failure(f"Status not updated correctly: {data.get('status')}")
            else:
                self.log_failure(f"Update task failed with status {response.status_code}")
                self.log_info(f"Response: {response.text}")
                
        except Exception as e:
            self.log_failure(f"Update task exception: {e}")
    
    def test_calendar_events(self):
        """Test 8: Get calendar events"""
        self.log_test("Calendar Events")
        
        try:
            response = requests.get(
                f"{API_V1}/calendar/events",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"Retrieved {len(data)} calendar event(s)")
                
                # Check if our task with deadline appears
                if self.created_task_id and data:
                    event_ids = [e.get("id") for e in data]
                    if self.created_task_id in event_ids:
                        self.log_success(f"Task with deadline appears in calendar")
                    else:
                        self.log_info(f"Task not in calendar (expected if status is completed)")
            else:
                self.log_failure(f"Calendar events failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Calendar events exception: {e}")
    
    def test_ai_analyze_task(self):
        """Test 9: AI task analysis"""
        self.log_test("AI Task Analysis")
        
        if not self.created_task_id:
            self.log_info("Skipping - no task ID available")
            return
        
        try:
            response = requests.post(
                f"{API_V1}/ai/analyze-task",
                json={"task_id": self.created_task_id},
                headers=self.get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_success(f"AI analysis completed")
                self.log_info(f"Estimated duration: {data.get('estimated_duration_minutes')} minutes")
                self.log_info(f"Tags: {data.get('suggested_tags')}")
            else:
                self.log_info(f"AI analysis endpoint returned {response.status_code}")
                self.log_info(f"Response: {response.text[:200]}")
                
        except Exception as e:
            self.log_info(f"AI analysis not fully configured or error: {e}")
    
    def test_delete_task(self):
        """Test 10: Delete a task"""
        self.log_test("Delete Task")
        
        if not self.created_task_id:
            self.log_info("Skipping - no task ID available")
            return
        
        try:
            response = requests.delete(
                f"{API_V1}/tasks/{self.created_task_id}",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_success(f"Task deleted successfully")
                
                # Verify deletion
                verify_response = requests.get(
                    f"{API_V1}/tasks/{self.created_task_id}",
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if verify_response.status_code == 404:
                    self.log_success(f"Verified task no longer exists")
                else:
                    self.log_failure(f"Task still exists after deletion")
            else:
                self.log_failure(f"Delete task failed with status {response.status_code}")
                
        except Exception as e:
            self.log_failure(f"Delete task exception: {e}")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}AI Planner Backend Integration Test Suite{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        self.test_health_check()
        self.test_root_endpoint()
        self.test_authentication()
        self.test_create_task()
        self.test_get_tasks()
        self.test_get_single_task()
        self.test_update_task()
        self.test_calendar_events()
        self.test_ai_analyze_task()
        self.test_delete_task()
        
        # Summary
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}Test Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"{Colors.BOLD}Total: {self.passed + self.failed}{Colors.RESET}")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] All tests passed!{Colors.RESET}\n")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}[FAILURE] Some tests failed{Colors.RESET}\n")
            return 1


def main():
    suite = IntegrationTestSuite()
    exit_code = suite.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

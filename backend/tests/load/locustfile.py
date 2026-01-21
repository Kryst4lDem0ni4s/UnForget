
from locust import HttpUser, task, between
import json


class AIWorkerUser(HttpUser):
    """Simulates a user interacting with the AI Planner API."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Setup - create a test user and get auth."""
        # In production, this would be real auth
        self.headers = {"Authorization": "Bearer test-user"}
        
        # Create a test user
        response = self.client.post(
            "/api/v1/users/",
            json={
                "email": f"loadtest{self.user_id}@example.com",
                "auth_provider_id": f"load-{self.user_id}"
            }
        )
        
        if response.status_code == 200:
            self.user_data = response.json()
    
    @task(3)
    def create_task(self):
        """Create a new task."""
        self.client.post(
            "/api/v1/tasks/",
            headers=self.headers,
            json={
                "title": "Load test task",
                "description": "Testing under load",
                "priority": "medium",
                "context_notes": "Automated load test"
            }
        )
    
    @task(5)
    def list_tasks(self):
        """List user's tasks."""
        self.client.get(
            "/api/v1/tasks/",
            headers=self.headers
        )
    
    @task(1)
    def get_user_profile(self):
        """Get current user profile."""
        self.client.get(
            "/api/v1/users/me",
            headers=self.headers
        )


class BurstTraffic(HttpUser):
    """Simulates burst traffic patterns."""
    
    wait_time = between(0.1, 0.5)  # Very short wait
    
    def on_start(self):
        self.headers = {"Authorization": "Bearer test-user"}
    
    @task
    def rapid_task_creation(self):
        """Rapidly create tasks to test queue handling."""
        for _ in range(10):
            self.client.post(
                "/api/v1/tasks/",
                headers=self.headers,
                json={"title": "Burst task"}
            )

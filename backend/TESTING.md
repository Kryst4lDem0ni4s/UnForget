# Testing Guide for AI Planner Backend

## Test Categories

### 1. Unit Tests
Test individual components in isolation.

**Run unit tests:**
```powershell
pytest tests/crud/ -v
```

### 2. API Integration Tests
Test API endpoints with database interactions.

**Run API tests:**
```powershell
pytest tests/api/ -v
```

### 3. Load/Stress Tests
Test system behavior under heavy load.

**Run load tests:**
```powershell
# Install locust if not already
pip install locust

# Start load test
locust -f tests/load/locustfile.py --host=http://localhost:8000

# Open browser to http://localhost:8089
# Configure: Users=100, Spawn rate=10
```

## Running All Tests

```powershell
# Run all tests with coverage
pytest --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## Test Database

Tests use an in-memory SQLite database that is created and destroyed for each test function. This ensures:
- Fast test execution
- Complete isolation between tests
- No side effects on development database

## Continuous Integration

For CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run tests
  run: |
    pip install -r requirements.txt -r requirements-test.txt
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Test Coverage Goals

- **Critical paths**: >90% (Auth, Task CRUD, User management)
- **API endpoints**: >80%
- **Overall**: >70%

## Performance Benchmarks

Expected performance under load (local dev):

- **Task creation**: <100ms p95
- **Task listing**: <50ms p95
- **User profile**: <30ms p95

**Throughput targets:**
- 100 concurrent users: <500ms response time
- 1000 requests/second: <1s response time

## Load Test Scenarios

### Scenario 1: Normal Load
- Users: 50
- Spawn rate: 5/sec
- Duration: 5 minutes

### Scenario 2: Burst Traffic
- Users: 200
- Spawn rate: 20/sec
- Duration: 2 minutes

### Scenario 3: Stress Test
- Users: 500
- Spawn rate: 50/sec
- Duration: 10 minutes

Monitor:
- Response times (p50, p95, p99)
- Error rate
- Database connection pool
- Memory usage

## Debugging Failed Tests

```powershell
# Run single test with verbose output
pytest tests/api/test_tasks.py::test_create_task -v -s

# Run with pdb debugger on failure
pytest --pdb

# Keep database after test for inspection
pytest --keep-db
```

## Mock External Services

For OAuth and calendar sync tests (not yet implemented):

```python
@pytest.fixture
def mock_google_calendar(monkeypatch):
    """Mock Google Calendar API."""
    def mock_list_events(*args, **kwargs):
        return {"items": []}
    
    monkeypatch.setattr(
        "app.services.calendar_sync.google.list_events",
        mock_list_events
    )
```

# PowerShell script to run comprehensive backend tests

Write-Host "AI Planner Backend Test Suite" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Cyan

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Install test dependencies
Write-Host "`nInstalling test dependencies..." -ForegroundColor Yellow
pip install -q -r requirements-test.txt

# Run unit tests
Write-Host "`n=== Running Unit Tests ===" -ForegroundColor Cyan
pytest tests/crud/ -v --tb=short

# Run API integration tests
Write-Host "`n=== Running API Integration Tests ===" -ForegroundColor Cyan
pytest tests/api/ -v --tb=short

# Run all tests with coverage
Write-Host "`n=== Running Full Test Suite with Coverage ===" -ForegroundColor Cyan
pytest --cov=app --cov-report=term --cov-report=html -v

Write-Host "`n=== Test Summary ===" -ForegroundColor Green
Write-Host " Unit tests completed"
Write-Host " Integration tests completed"
Write-Host " Coverage report generated (see htmlcov/index.html)"
Write-Host "`nTo run load tests:"
Write-Host "  locust -f tests/load/locustfile.py --host=http://localhost:8000" -ForegroundColor Yellow

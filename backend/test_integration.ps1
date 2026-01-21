$Headers = @{
    "Authorization" = "Bearer test-user"
    "Content-Type" = "application/json"
}

$BaseUrl = "http://localhost:8000/api/v1"

Write-Host "1. Creating Task..."
$TaskBody = @{
    title = "Test Integration Task"
    description = "Verify the AI pipeline works end to end"
    context_notes = "This is a critical test. Needs to happen ASAP."
    priority = "high"
} | ConvertTo-Json

try {
    $TaskResponse = Invoke-RestMethod -Uri "$BaseUrl/tasks/" -Method Post -Headers $Headers -Body $TaskBody
    $TaskId = $TaskResponse.id
    Write-Host "Task Created: $TaskId"
} catch {
    Write-Error "Failed to create task: $_"
    exit 1
}

Write-Host "`n2. Analyzing Task (AI)..."
$AnalyzeBody = @{
    task_id = $TaskId
} | ConvertTo-Json

try {
    $AnalyzeResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/analyze-task" -Method Post -Headers $Headers -Body $AnalyzeBody
    Write-Host "Analysis Result:"
    $AnalyzeResponse | ConvertTo-Json -Depth 5
} catch {
    Write-Error "Failed to analyze task: $_"
    exit 1
}

Write-Host "`n3. Scheduling Task (AI)..."
# Using same body as analyze
try {
    $ScheduleResponse = Invoke-RestMethod -Uri "$BaseUrl/ai/schedule" -Method Post -Headers $Headers -Body $AnalyzeBody
    Write-Host "Scheduling Options:"
    $ScheduleResponse | ConvertTo-Json -Depth 5
} catch {
    Write-Error "Failed to schedule task: $_"
    exit 1
}

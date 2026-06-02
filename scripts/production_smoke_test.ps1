# KRONOS CORE — Production Smoke Test
# Edit $BaseUrl and $FrontendUrl before running.
# Run with: pwsh scripts/production_smoke_test.ps1

param(
    [string]$BaseUrl     = "http://127.0.0.1:8000",
    [string]$FrontendUrl = "http://localhost:3000"
)

$pass  = 0
$fail  = 0
$tests = @()

function Test-Endpoint {
    param([string]$Label, [string]$Url, [int]$Expected = 200)
    try {
        $resp = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        $ok   = $resp.StatusCode -eq $Expected
        $icon = if ($ok) { "[PASS]" } else { "[FAIL]" }
        Write-Host "$icon  $Label  ($($resp.StatusCode))"
        return $ok
    } catch {
        Write-Host "[FAIL]  $Label  (error: $($_.Exception.Message))"
        return $false
    }
}

Write-Host ""
Write-Host "====================================="
Write-Host "  KRONOS CORE — Production Smoke Test"
Write-Host "  Backend : $BaseUrl"
Write-Host "  Frontend: $FrontendUrl"
Write-Host "====================================="
Write-Host ""

$tests += Test-Endpoint "Backend health"       "$BaseUrl/api/v1/health"
$tests += Test-Endpoint "API root"             "$BaseUrl/api/v1/"
$tests += Test-Endpoint "API docs (Swagger)"   "$BaseUrl/docs"
$tests += Test-Endpoint "Billing status"       "$BaseUrl/api/v1/billing/status"
$tests += Test-Endpoint "Billing plans"        "$BaseUrl/api/v1/billing/plans"
$tests += Test-Endpoint "History root"         "$BaseUrl/api/v1/history"
$tests += Test-Endpoint "Enterprise report"    "$BaseUrl/api/v1/enterprise/report"
$tests += Test-Endpoint "Auth status"          "$BaseUrl/api/v1/auth/status"
$tests += Test-Endpoint "PDF export"           "$BaseUrl/api/v1/export/enterprise/pdf"
$tests += Test-Endpoint "Frontend home"        "$FrontendUrl"

$pass = ($tests | Where-Object { $_ -eq $true }).Count
$fail = ($tests | Where-Object { $_ -eq $false }).Count

Write-Host ""
Write-Host "====================================="
Write-Host "  Results: $pass passed, $fail failed"
Write-Host "====================================="

if ($fail -gt 0) {
    Write-Host ""
    Write-Host "  One or more checks failed. Verify:"
    Write-Host "  - Backend is running:  uvicorn app.main:app --host 0.0.0.0 --port 8000"
    Write-Host "  - Frontend is running: cd frontend && npm run dev"
    Write-Host "  - Production env vars are set in .env"
    exit 1
}

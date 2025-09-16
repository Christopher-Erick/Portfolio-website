# Docker Health Check Script for Windows
# This script verifies that all services are running correctly

Write-Host "Checking Docker deployment health..." -ForegroundColor Green

# Check if docker-compose is installed
try {
    $dockerComposeVersion = docker-compose --version
    Write-Host "Docker Compose found: $dockerComposeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: docker-compose not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if services are running
Write-Host "Checking if services are running..." -ForegroundColor Yellow
docker-compose ps

# Check web service
Write-Host "Checking web service..." -ForegroundColor Yellow
$webStatus = docker-compose ps | Select-String -Pattern "web" | Select-String -Pattern "Up|running"
if ($null -eq $webStatus) {
    Write-Host "Error: Web service is not running" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Web service is running" -ForegroundColor Green
}

# Check database service
Write-Host "Checking database service..." -ForegroundColor Yellow
$dbStatus = docker-compose ps | Select-String -Pattern "db" | Select-String -Pattern "Up|running"
if ($null -eq $dbStatus) {
    Write-Host "Error: Database service is not running" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Database service is running" -ForegroundColor Green
}

# Check nginx service
Write-Host "Checking nginx service..." -ForegroundColor Yellow
$nginxStatus = docker-compose ps | Select-String -Pattern "nginx" | Select-String -Pattern "Up|running"
if ($null -eq $nginxStatus) {
    Write-Host "Error: Nginx service is not running" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Nginx service is running" -ForegroundColor Green
}

# Check if we can access the application
Write-Host "Checking application accessibility..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Application is accessible at http://localhost" -ForegroundColor Green
    } else {
        Write-Host "Warning: Application returned status code $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Warning: Could not access application at http://localhost" -ForegroundColor Yellow
    Write-Host "This might be OK if the application is still starting up" -ForegroundColor Yellow
}

Write-Host "Health check completed." -ForegroundColor Green
Write-Host "To view logs, run: docker-compose logs" -ForegroundColor Cyan
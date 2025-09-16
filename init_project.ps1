# Initialization script for the cybersecurity portfolio project (Windows version)
# This script helps with the initial setup of the project

Write-Host "Initializing Cybersecurity Portfolio Project..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: manage.py not found. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}

# Check if Docker is available
try {
    $dockerVersion = docker --version
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
    
    # Copy environment file if it doesn't exist
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file from development template..." -ForegroundColor Yellow
        Copy-Item ".env.development" ".env"
        Write-Host "Please edit .env file to configure your settings." -ForegroundColor Cyan
    } else {
        Write-Host ".env file already exists." -ForegroundColor Green
    }
    
    # Build and start Docker containers
    Write-Host "Building and starting Docker containers..." -ForegroundColor Yellow
    docker-compose up --build -d
    
    # Wait for services to start
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Run initial setup
    Write-Host "Running initial setup..." -ForegroundColor Yellow
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py collectstatic --noinput
    
    Write-Host "Docker setup complete!" -ForegroundColor Green
    Write-Host "Access your application at http://localhost" -ForegroundColor Cyan
}
catch {
    Write-Host "Docker not found. Setting up standard Python environment..." -ForegroundColor Yellow
    
    # Check if virtual environment exists
    if (-not (Test-Path "venv")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    
    # Install dependencies
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Run migrations
    Write-Host "Running database migrations..." -ForegroundColor Yellow
    python manage.py migrate
    
    # Collect static files
    Write-Host "Collecting static files..." -ForegroundColor Yellow
    python manage.py collectstatic --noinput
    
    Write-Host "Standard setup complete!" -ForegroundColor Green
    Write-Host "Run 'python manage.py runserver' to start the development server." -ForegroundColor Cyan
}

Write-Host "Initialization complete!" -ForegroundColor Green
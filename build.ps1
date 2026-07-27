# PowerShell build script for Windows environments
# exit on error
$ErrorActionPreference = "Stop"

Write-Host "Creating logs directory if it doesn't exist..."
New-Item -ItemType Directory -Path "logs" -Force

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
Write-Host "Running migrations..."
python manage.py migrate

# Create cache table for database cache (fallback if Redis is not available)
Write-Host "Creating cache table..."
try {
    python manage.py createcachetable
} catch {
    Write-Host "Failed to create cache table, continuing..."
}

# Populate database with initial data
Write-Host "Populating database with initial data..."
python post_deploy.py

Write-Host "Build completed successfully!"
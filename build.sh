#!/bin/bash
# exit on error
set -o errexit

# NOTE: When deploying to Unix-based systems, ensure this file has executable permissions (100755)
# chmod +x build.sh

# Create logs directory if it doesn't exist
echo "Creating logs directory if it doesn't exist..."
mkdir -p logs

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create cache table for database cache (fallback if Redis is not available)
echo "Creating cache table..."
python manage.py createcachetable || echo "Failed to create cache table, continuing..."

# Populate database with initial data
echo "Populating database with initial data..."
python post_deploy.py

echo "Build completed successfully!"
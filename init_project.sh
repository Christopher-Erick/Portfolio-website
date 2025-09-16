#!/bin/bash

# Initialization script for the cybersecurity portfolio project
# This script helps with the initial setup of the project

echo "Initializing Cybersecurity Portfolio Project..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "Docker found. Setting up Docker environment..."
    
    # Copy environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        echo "Creating .env file from development template..."
        cp .env.development .env
        echo "Please edit .env file to configure your settings."
    else
        echo ".env file already exists."
    fi
    
    # Build and start Docker containers
    echo "Building and starting Docker containers..."
    docker-compose up --build -d
    
    # Wait for services to start
    echo "Waiting for services to start..."
    sleep 10
    
    # Run initial setup
    echo "Running initial setup..."
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py collectstatic --noinput
    
    echo "Docker setup complete!"
    echo "Access your application at http://localhost"
else
    echo "Docker not found. Setting up standard Python environment..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run migrations
    echo "Running database migrations..."
    python manage.py migrate
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    echo "Standard setup complete!"
    echo "Run 'python manage.py runserver' to start the development server."
fi

echo "Initialization complete!"
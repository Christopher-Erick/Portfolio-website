#!/bin/bash

# Docker Health Check Script
# This script verifies that all services are running correctly

echo "Checking Docker deployment health..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Error: docker-compose not found. Please install Docker Compose."
    exit 1
fi

# Check if services are running
echo "Checking if services are running..."
docker-compose ps

# Check web service
echo "Checking web service..."
WEB_STATUS=$(docker-compose ps | grep web | grep -E "(Up|running)")
if [ -z "$WEB_STATUS" ]; then
    echo "Error: Web service is not running"
    exit 1
else
    echo "✓ Web service is running"
fi

# Check database service
echo "Checking database service..."
DB_STATUS=$(docker-compose ps | grep db | grep -E "(Up|running)")
if [ -z "$DB_STATUS" ]; then
    echo "Error: Database service is not running"
    exit 1
else
    echo "✓ Database service is running"
fi

# Check nginx service
echo "Checking nginx service..."
NGINX_STATUS=$(docker-compose ps | grep nginx | grep -E "(Up|running)")
if [ -z "$NGINX_STATUS" ]; then
    echo "Error: Nginx service is not running"
    exit 1
else
    echo "✓ Nginx service is running"
fi

# Check if we can access the application
echo "Checking application accessibility..."
curl -f http://localhost > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Application is accessible at http://localhost"
else
    echo "Warning: Could not access application at http://localhost"
    echo "This might be OK if the application is still starting up"
fi

echo "Health check completed."
echo "To view logs, run: docker-compose logs"
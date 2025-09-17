@echo off
REM exit on error
setlocal enabledelayedexpansion

REM Create logs directory if it doesn't exist
echo Creating logs directory if it doesn't exist...
mkdir logs 2>nul

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --no-input

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create cache table for database cache (fallback if Redis is not available)
echo Creating cache table...
python manage.py createcachetable || echo Failed to create cache table, continuing...

REM Populate database with initial data
echo Populating database with initial data...
python post_deploy.py

echo Build completed successfully!
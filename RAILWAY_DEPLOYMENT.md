# Railway Deployment Guide

## Prerequisites

1. Railway account (you already have one)
2. This repository connected to Railway

## Deployment Steps

1. Connect your GitHub repository to Railway:
   - Go to your Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose this repository

2. Configure environment variables:
   - In your Railway project, go to the "Variables" tab
   - Add the following environment variables:
     ```
     SECRET_KEY=your-very-secure-secret-key
     DEBUG=False
     DATABASE_URL=postgresql://postgres:WWdivubBcdCYXrkmsfMbJmoxxmAPgRZQ@crossover.proxy.rlwy.net:40839/railway
     ALLOWED_HOSTS=your-app-name.up.railway.app,railway.app
     ```

3. Configure the start command:
   - Railway should automatically detect the start command from your Dockerfile or railway.toml
   - If not, set it manually to:
     ```
     gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:$PORT
     ```

4. Deploy the application:
   - Railway will automatically deploy when you push to your connected GitHub repository
   - Or trigger a manual deploy from the Railway dashboard

5. Run initial migrations:
   - Go to the "Deployments" tab in Railway
   - Click on the latest deployment
   - Click "Console" to open a terminal
   - Run:
     ```
     python manage.py migrate
     ```

6. Create a superuser:
   - In the same console, run:
     ```
     python manage.py createsuperuser
     ```

7. Collect static files:
   - In the console, run:
     ```
     python manage.py collectstatic --noinput
     ```

## Environment Variables

Make sure to set these environment variables in your Railway project:

- `SECRET_KEY` - Your Django secret key (generate a secure one)
- `DEBUG` - Set to `False` for production
- `DATABASE_URL` - Your Railway PostgreSQL database URL
- `ALLOWED_HOSTS` - Your Railway app URL (e.g., `your-app-name.up.railway.app,railway.app`)

## Custom Domain (Optional)

If you want to use a custom domain:

1. In your Railway project, go to "Settings" → "Domains"
2. Add your custom domain
3. Follow Railway's instructions to configure DNS

## Scaling

Railway automatically scales your application based on traffic. You can also manually configure scaling options in the "Settings" tab.
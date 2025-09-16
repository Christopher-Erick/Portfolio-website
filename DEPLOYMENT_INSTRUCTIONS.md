# Deployment Instructions for Fly.io and Railway

## Railway Database Setup

1. Create a PostgreSQL database on Railway:
   - Go to https://railway.app/
   - Sign up or log in to your Railway account
   - Create a new project
   - Add a new service and select "Database" → "PostgreSQL"

2. Get the database connection URL:
   - In your Railway dashboard, select your PostgreSQL database
   - Go to the "Connect" tab
   - Copy the "Connection URL" which will look like:
     `postgresql://username:password@host:port/database_name`

3. Update your [.env](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\manage.py#L10-L10) file:
   - Replace the DATABASE_URL value with the one you copied from Railway
   - Update other values as needed (SECRET_KEY, ALLOWED_HOSTS, etc.)

4. Run migrations to set up your database tables:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for your admin panel:
   ```bash
   python manage.py createsuperuser
   ```

## Fly.io Application Deployment

1. Install the Fly.io CLI:
   - Download from https://fly.io/docs/getting-started/installing-flyctl/

2. Log in to Fly.io:
   ```bash
   flyctl auth login
   ```

3. Launch your application:
   ```bash
   flyctl launch
   ```
   - Choose a name for your app
   - Select a region close to your target audience
   - Don't deploy yet when prompted

4. Set environment variables on Fly.io:
   ```bash
   flyctl secrets set SECRET_KEY="your-secret-key"
   flyctl secrets set DATABASE_URL="your-railway-database-url"
   flyctl secrets set DEBUG=False
   # Add other environment variables as needed
   ```

5. Deploy your application:
   ```bash
   flyctl deploy
   ```

6. Run migrations on Fly.io:
   ```bash
   flyctl ssh console
   # Then run:
   python manage.py migrate
   ```

7. Create a superuser on Fly.io:
   ```bash
   flyctl ssh console
   # Then run:
   python manage.py createsuperuser
   ```

## Updating Your Application

To update your application after making changes:

1. Commit and push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

2. Deploy to Fly.io:
   ```bash
   flyctl deploy
   ```

## Useful Commands

- Check application status: `flyctl status`
- View application logs: `flyctl logs`
- Access the console: `flyctl ssh console`
- Scale your application: `flyctl scale count 2` (to run 2 instances)
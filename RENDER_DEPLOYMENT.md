# Render Deployment Guide

## Prerequisites

1. Render account (sign up at https://render.com/)
2. This repository connected to Render

## Deployment Steps

1. Connect your GitHub repository to Render:
   - Go to your Render dashboard
   - Click "New Web Service"
   - Connect your GitHub account if not already connected
   - Select this repository

2. Configure the web service:
   - Name: christopher-erick-otieno-portfolio
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:$PORT`
   - Instance Type: Free (for testing) or Starter/Standard for production

3. Add environment variables:
   - In the "Environment Variables" section, add:
     ```
     SECRET_KEY=your-very-secure-secret-key
     DEBUG=False
     DATABASE_URL=postgresql://postgres:WWdivubBcdCYXrkmsfMbJmoxxmAPgRZQ@crossover.proxy.rlwy.net:40839/railway
     ALLOWED_HOSTS=your-app-name.onrender.com,render.app
     ```

4. Configure the database:
   - Since you're using Railway for your database, you don't need to create a new database on Render
   - Just make sure your DATABASE_URL points to your Railway PostgreSQL instance

5. Deploy the application:
   - Click "Create Web Service"
   - Render will automatically start building and deploying your application
   - This process may take 5-10 minutes

6. Monitor the deployment:
   - Watch the build logs in the Render dashboard
   - Once deployed, your application will be available at:
     `https://christopher-erick-otieno-portfolio.onrender.com`

## Environment Variables

Make sure to set these environment variables in your Render web service:

- `SECRET_KEY` - Your Django secret key (generate a secure one)
- `DEBUG` - Set to `False` for production
- `DATABASE_URL` - Your Railway PostgreSQL database URL
- `ALLOWED_HOSTS` - Your Render app URL (e.g., `christopher-erick-otieno-portfolio.onrender.com,render.app`)
- `RENDER_EXTERNAL_HOSTNAME` - Your Render app hostname (optional)

## Custom Domain (Optional)

If you want to use a custom domain:

1. In your Render web service, go to "Settings" → "Custom Domains"
2. Add your custom domain
3. Follow Render's instructions to configure DNS

## Automatic Deployments

Render automatically redeploys your application when you push changes to your GitHub repository.

## Scaling

Render's free tier includes:
- 750 free hours per month (about 31 days)
- Sleeps after 15 minutes of inactivity
- Takes a few seconds to spin up when accessed after sleeping

For production use, consider upgrading to a paid plan to avoid the sleep behavior.

## Troubleshooting

1. If your application fails to build:
   - Check the build logs for specific error messages
   - Ensure all dependencies are listed in requirements.txt

2. If your application deploys but doesn't respond:
   - Check that your ALLOWED_HOSTS includes your Render URL
   - Verify your database connection settings

3. If static files aren't loading:
   - Make sure collectstatic is run during the build process
   - Check that DEBUG is set to False

## Useful Render Commands

- View logs: Available in the Render dashboard
- Access console: Available in the Render dashboard
- Redeploy: Trigger a manual deploy from the dashboard
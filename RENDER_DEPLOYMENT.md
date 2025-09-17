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

### Common Issues and Solutions

1. **Repository Connection Issues**
   - Ensure your repository is public or you've granted Render access to private repositories
   - Check that the repository URL is correct in Render
   - Try disconnecting and reconnecting your GitHub account in Render settings

2. **Build Script Failures**
   - Check the build logs in Render for specific error messages
   - Ensure your [build.sh](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\build.sh) file has the correct permissions (should be executable)
   - Verify all dependencies in [requirements.txt](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\requirements.txt) are correct and available
   - The build script should be committed with executable permissions (`100755` in Git)
   - If you encounter permission issues, you can use the `set_permissions.sh` script to fix them
   - For cross-platform compatibility, the project includes both `build.sh` (Unix/Linux) and `build.bat` (Windows) scripts

3. **Environment Variable Issues**
   - Make sure you've set all required environment variables in Render:
     - [SECRET_KEY](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L36-L36)
     - [DEBUG](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L43-L43) (set to False)
     - [DATABASE_URL](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L135-L135)
     - [ALLOWED_HOSTS](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L46-L46)

4. **Database Connection Issues**
   - Verify your [DATABASE_URL](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L135-L135) is correct
   - Check that your Railway database is running and accessible
   - Make sure the database credentials haven't expired

5. **Django Settings Issues**
   - Check that [ALLOWED_HOSTS](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L46-L46) includes your Render URL
   - Ensure [DEBUG](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\portfolio_site\settings.py#L43-L43) is set to False in production
   - Verify static files configuration

6. **Application Startup Issues**
   - Check that your start command is correct: `gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:$PORT`
   - Ensure the PORT environment variable is being used correctly
   - Verify that your WSGI application is properly configured

### Debugging Steps

1. **Check Build Logs**
   - In your Render dashboard, go to your web service
   - Click on the "Logs" tab
   - Look for error messages during the build process

2. **Check Application Logs**
   - After deployment, check the application logs for runtime errors
   - Look for Django-specific errors or database connection issues

3. **Test Locally**
   - Try running your application locally with the same environment variables
   - This can help identify configuration issues before deploying

4. **Verify Dependencies**
   - Ensure all required packages are listed in [requirements.txt](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\requirements.txt)
   - Check for version conflicts between packages

## Useful Render Commands

- View logs: Available in the Render dashboard
- Access console: Available in the Render dashboard
- Redeploy: Trigger a manual deploy from the dashboard
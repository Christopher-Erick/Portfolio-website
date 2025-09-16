# Production Environment Setup Script for Windows
# This script helps set up a production-ready environment for the portfolio website.

function Generate-SecretKey {
    param(
        [int]$Length = 50
    )
    
    # Characters to use for the secret key
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?~|{}[]:;,.\/"
    
    # Convert to character array
    $charArray = $chars.ToCharArray()
    
    # Generate the secret key
    $secretKey = ""
    for ($i = 0; $i -lt $Length; $i++) {
        $randomIndex = Get-Random -Minimum 0 -Maximum $charArray.Length
        $secretKey += $charArray[$randomIndex]
    }
    
    return $secretKey
}

function Setup-ProductionEnv {
    Write-Host "Setting up production environment..." -ForegroundColor Green
    
    # Check if .env.production exists
    $envFile = ".env.production"
    if (-not (Test-Path $envFile)) {
        Write-Host "Error: .env.production file not found!" -ForegroundColor Red
        return $false
    }
    
    # Generate a secure secret key
    $secretKey = Generate-SecretKey
    
    # Display what needs to be configured
    Write-Host ""
    Write-Host "=== Production Environment Setup ===" -ForegroundColor Cyan
    Write-Host "The following values need to be configured in your .env.production file:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. SECRET_KEY:" -ForegroundColor Yellow
    Write-Host "   $secretKey" -ForegroundColor White
    Write-Host ""
    Write-Host "2. POSTGRES_PASSWORD:" -ForegroundColor Yellow
    Write-Host "   Set a secure password for your PostgreSQL database" -ForegroundColor White
    Write-Host ""
    Write-Host "3. ALLOWED_HOSTS:" -ForegroundColor Yellow
    Write-Host "   Set your actual domain (e.g., yourdomain.com,www.yourdomain.com)" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Email Configuration:" -ForegroundColor Yellow
    Write-Host "   - EMAIL_HOST: Your SMTP server" -ForegroundColor White
    Write-Host "   - EMAIL_HOST_USER: Your email address" -ForegroundColor White
    Write-Host "   - EMAIL_HOST_PASSWORD: Your app-specific password" -ForegroundColor White
    Write-Host "   - CONTACT_EMAIL: Your contact email" -ForegroundColor White
    Write-Host ""
    Write-Host "After updating these values, copy .env.production to .env:" -ForegroundColor Yellow
    Write-Host "copy .env.production .env" -ForegroundColor White
    Write-Host ""
    
    # Save the generated secret key to a file for easy access
    $secretKey | Out-File -FilePath ".secret_key" -Encoding UTF8
    
    Write-Host "A secret key has been generated and saved to .secret_key" -ForegroundColor Green
    Write-Host "Please update your .env.production file with this key and other required values." -ForegroundColor Cyan
    
    return $true
}

function Check-ProductionReadiness {
    Write-Host "Checking production readiness..." -ForegroundColor Green
    
    # Check if required files exist
    $requiredFiles = @(
        "Dockerfile",
        "docker-compose.yml",
        "config/nginx/nginx.conf",
        ".env.production"
    )
    
    $missingFiles = @()
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Host "❌ Missing required files:" -ForegroundColor Red
        foreach ($file in $missingFiles) {
            Write-Host "   - $file" -ForegroundColor Red
        }
        return $false
    }
    
    # Check if config/certs directory exists
    if (-not (Test-Path "config/certs")) {
        Write-Host "⚠️  Warning: config/certs directory not found" -ForegroundColor Yellow
        Write-Host "   You need to set up SSL certificates for production" -ForegroundColor Yellow
    }
    
    # Check if .env.production has been updated
    $content = Get-Content ".env.production" -Raw
    
    $placeholders = @(
        "your-super-secret-key-here",
        "your-secure-database-password-here",
        "yourdomain.com",
        "your-email@gmail.com",
        "your-app-specific-password"
    )
    
    $unfilledPlaceholders = @()
    foreach ($placeholder in $placeholders) {
        if ($content -like "*$placeholder*") {
            $unfilledPlaceholders += $placeholder
        }
    }
    
    if ($unfilledPlaceholders.Count -gt 0) {
        Write-Host "⚠️  Warning: The following placeholders still need to be filled in .env.production:" -ForegroundColor Yellow
        foreach ($placeholder in $unfilledPlaceholders) {
            Write-Host "   - $placeholder" -ForegroundColor Yellow
        }
        return $false
    }
    
    Write-Host "✅ All required files are present" -ForegroundColor Green
    Write-Host "✅ Basic production setup appears to be complete" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Generate SSL certificates" -ForegroundColor White
    Write-Host "2. Copy .env.production to .env" -ForegroundColor White
    Write-Host "3. Run: docker-compose up --build" -ForegroundColor White
    Write-Host "4. Run initial setup commands" -ForegroundColor White
    
    return $true
}

# Main execution
if ($args.Count -gt 0 -and $args[0] -eq "check") {
    Check-ProductionReadiness
} else {
    Setup-ProductionEnv
}
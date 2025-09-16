# Production Setup Verification Script for Windows
# This script verifies that all components are properly configured for production deployment.

function Check-FileStructure {
    Write-Host "Checking file structure..." -ForegroundColor Yellow
    
    $requiredPaths = @(
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        "manage.py",
        "config/nginx/nginx.conf",
        "config/certs",
        ".env.production",
        ".env.development"
    )
    
    $missingPaths = @()
    foreach ($path in $requiredPaths) {
        if (-not (Test-Path $path)) {
            $missingPaths += $path
        }
    }
    
    if ($missingPaths.Count -gt 0) {
        Write-Host "❌ Missing required paths:" -ForegroundColor Red
        foreach ($path in $missingPaths) {
            Write-Host "   - $path" -ForegroundColor Red
        }
        return $false
    }
    
    Write-Host "✅ All required files and directories are present" -ForegroundColor Green
    return $true
}

function Check-DockerCompose {
    Write-Host "Checking Docker Compose configuration..." -ForegroundColor Yellow
    
    try {
        $content = Get-Content "docker-compose.yml" -Raw
        
        $requiredSections = @(
            "services:",
            "web:",
            "db:",
            "nginx:",
            "volumes:",
            "networks:"
        )
        
        $missingSections = @()
        foreach ($section in $requiredSections) {
            if ($content -notlike "*$section*") {
                $missingSections += $section
            }
        }
        
        if ($missingSections.Count -gt 0) {
            Write-Host "❌ Missing sections in docker-compose.yml:" -ForegroundColor Red
            foreach ($section in $missingSections) {
                Write-Host "   - $section" -ForegroundColor Red
            }
            return $false
        }
        
        Write-Host "✅ Docker Compose configuration is complete" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error reading docker-compose.yml: $_" -ForegroundColor Red
        return $false
    }
}

function Check-NginxConfig {
    Write-Host "Checking Nginx configuration..." -ForegroundColor Yellow
    
    try {
        $content = Get-Content "config/nginx/nginx.conf" -Raw
        
        $requiredSections = @(
            "upstream django",
            "server {",
            "listen 80",
            "listen 443 ssl",
            "proxy_pass http://django"
        )
        
        $missingSections = @()
        foreach ($section in $requiredSections) {
            if ($content -notlike "*$section*") {
                $missingSections += $section
            }
        }
        
        if ($missingSections.Count -gt 0) {
            Write-Host "❌ Missing sections in nginx.conf:" -ForegroundColor Red
            foreach ($section in $missingSections) {
                Write-Host "   - $section" -ForegroundColor Red
            }
            return $false
        }
        
        Write-Host "✅ Nginx configuration is complete" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error reading nginx.conf: $_" -ForegroundColor Red
        return $false
    }
}

function Check-EnvironmentTemplates {
    Write-Host "Checking environment templates..." -ForegroundColor Yellow
    
    try {
        # Check development template
        $devContent = Get-Content ".env.development" -Raw
        
        # Check production template
        $prodContent = Get-Content ".env.production" -Raw
        
        # Verify personal information is preserved
        $personalInfo = @(
            "Christopher Erick Otieno",
            "erikchris54@gmail.com",
            "+254758081580",
            "Nairobi, Kenya",
            "Christopher-Erick",
            "erikchris54",
            "ChristopherErick"
        )
        
        $missingInfo = @()
        foreach ($info in $personalInfo) {
            if ($prodContent -notlike "*$info*") {
                $missingInfo += $info
            }
        }
        
        if ($missingInfo.Count -gt 0) {
            Write-Host "❌ Missing personal information in .env.production:" -ForegroundColor Red
            foreach ($info in $missingInfo) {
                Write-Host "   - $info" -ForegroundColor Red
            }
            return $false
        }
        
        Write-Host "✅ Personal information is preserved in environment templates" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error checking environment templates: $_" -ForegroundColor Red
        return $false
    }
}

function Check-Requirements {
    Write-Host "Checking Python requirements..." -ForegroundColor Yellow
    
    try {
        $content = Get-Content "requirements.txt" -Raw
        
        $requiredPackages = @(
            "Django",
            "Pillow",
            "reportlab",
            "whitenoise",
            "gunicorn",
            "psycopg2-binary"
        )
        
        $missingPackages = @()
        foreach ($package in $requiredPackages) {
            if ($content -notlike "*$package*") {
                $missingPackages += $package
            }
        }
        
        if ($missingPackages.Count -gt 0) {
            Write-Host "❌ Missing packages in requirements.txt:" -ForegroundColor Red
            foreach ($package in $missingPackages) {
                Write-Host "   - $package" -ForegroundColor Red
            }
            return $false
        }
        
        Write-Host "✅ All required Python packages are listed" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error reading requirements.txt: $_" -ForegroundColor Red
        return $false
    }
}

function Main {
    Write-Host "=== Production Setup Verification ===" -ForegroundColor Cyan
    Write-Host ""
    
    $checks = @(
        @{Name = "Check-FileStructure"; Func = ${function:Check-FileStructure}},
        @{Name = "Check-DockerCompose"; Func = ${function:Check-DockerCompose}},
        @{Name = "Check-NginxConfig"; Func = ${function:Check-NginxConfig}},
        @{Name = "Check-EnvironmentTemplates"; Func = ${function:Check-EnvironmentTemplates}},
        @{Name = "Check-Requirements"; Func = ${function:Check-Requirements}}
    )
    
    $allPassed = $true
    foreach ($check in $checks) {
        if (-not (& $check.Func)) {
            $allPassed = $false
        }
        Write-Host ""
    }
    
    if ($allPassed) {
        Write-Host "🎉 All checks passed! Your application is ready for production setup." -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Generate a secure secret key: .\setup_production.ps1" -ForegroundColor White
        Write-Host "2. Update .env.production with your actual values" -ForegroundColor White
        Write-Host "3. Copy .env.production to .env: copy .env.production .env" -ForegroundColor White
        Write-Host "4. Generate SSL certificates" -ForegroundColor White
        Write-Host "5. Run: docker-compose up --build" -ForegroundColor White
        Write-Host "6. Run initial setup commands" -ForegroundColor White
        Write-Host "7. Test all functionality" -ForegroundColor White
        return 0
    } else {
        Write-Host "❌ Some checks failed. Please review the issues above." -ForegroundColor Red
        Write-Host "See PRODUCTION_CHECKLIST.md for detailed instructions." -ForegroundColor Yellow
        return 1
    }
}

# Main execution
exit (Main)
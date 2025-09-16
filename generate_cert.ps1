# Script to generate self-signed SSL certificates for development on Windows
# Run this script from the project root directory

Write-Host "Generating self-signed SSL certificates for development..."

# Create certificates directory if it doesn't exist
if (!(Test-Path -Path "config\certs")) {
    New-Item -ItemType Directory -Path "config\certs" | Out-Null
}

# Check if OpenSSL is available
try {
    $opensslVersion = openssl version
    Write-Host "OpenSSL found: $opensslVersion"
} catch {
    Write-Host "Error: OpenSSL not found. Please install OpenSSL and make sure it's in your PATH."
    Write-Host "You can download OpenSSL from: https://slproweb.com/products/Win32OpenSSL.html"
    exit 1
}

# Generate private key
openssl genrsa -out config/certs/key.pem 2048

# Generate certificate
openssl req -new -x509 -key config/certs/key.pem -out config/certs/cert.pem -days 365 -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

Write-Host "SSL certificates generated successfully!" -ForegroundColor Green
Write-Host "Certificate: config/certs/cert.pem"
Write-Host "Private Key: config/certs/key.pem"
Write-Host ""
Write-Host "IMPORTANT: These are self-signed certificates for development only." -ForegroundColor Yellow
Write-Host "Do not use them in production. Use certificates from a trusted CA instead."
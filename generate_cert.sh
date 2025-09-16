#!/bin/bash

# Script to generate self-signed SSL certificates for development
# Run this script from the project root directory

echo "Generating self-signed SSL certificates for development..."

# Create certificates directory if it doesn't exist
mkdir -p config/certs

# Generate private key
openssl genrsa -out config/certs/key.pem 2048

# Generate certificate
openssl req -new -x509 -key config/certs/key.pem -out config/certs/cert.pem -days 365 -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "SSL certificates generated successfully!"
echo "Certificate: config/certs/cert.pem"
echo "Private Key: config/certs/key.pem"
echo ""
echo "IMPORTANT: These are self-signed certificates for development only."
echo "Do not use them in production. Use certificates from a trusted CA instead."
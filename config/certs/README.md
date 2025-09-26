# SSL Certificates Directory

This directory is intended to store SSL certificates for HTTPS configuration.

## For Development/Testing

For development and testing purposes, you can generate self-signed certificates using OpenSSL:

```bash
# Generate a private key
openssl genrsa -out key.pem 2048

# Generate a certificate
openssl req -new -x509 -key key.pem -out cert.pem -days 365
```

## For Production

For production environments, you should obtain proper SSL certificates from a Certificate Authority (CA) such as:
- Let's Encrypt (free)
- DigiCert
- Comodo
- GoDaddy

Place your certificate files in this directory:
- `cert.pem` - The certificate file
- `key.pem` - The private key file

Make sure to set appropriate permissions on the private key file to protect it.
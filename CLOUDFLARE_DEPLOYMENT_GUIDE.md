# 🚀 Cloudflare Production Deployment & Security Guide

This project is fully configured and optimized for **exclusive deployment on Cloudflare** using **Cloudflare Tunnel (`cloudflared`)**, **Cloudflare R2 Storage**, **Cloudflare WAF / Edge Security**, and **Cloudflare DNS/CDN**.

---

## 🏗️ Architecture Overview

```
                          [ Cloudflare Edge ]
                       (DNS + WAF + DDoS + CDN)
                                  │
                                  ▼ (Zero Trust Encrypted Tunnel)
                   [ Cloudflare Tunnel (cloudflared) ]
                                  │
                                  ▼
                        [ Docker Container ]
                      (Gunicorn WSGI + Django)
                                  │
                      ┌───────────┴───────────┐
                      ▼                       ▼
            [ PostgreSQL Database ]   [ Cloudflare R2 Storage ]
                                      (Zero Egress Media Assets)
```

- **Zero Open Ports**: The server does NOT expose any public inbound ports (no port 80/443 open to the public internet). Traffic is securely tunneled out to Cloudflare via `cloudflared`.
- **Media Assets**: Uploads (CV, project screenshots, images) are served through **Cloudflare R2** with zero egress fees.
- **Edge Protection**: Cloudflare WAF, DDoS mitigation, SSL/TLS encryption, HTTP/3, and Bot Management operate seamlessly at the Cloudflare edge.

---

## 📋 Prerequisites

1. A **Cloudflare Account** with your domain added (nameservers pointed to Cloudflare).
2. **Docker** and **Docker Compose** installed on your server/host.
3. A **Cloudflare R2 Bucket** created in your Cloudflare Dashboard (e.g. `portfolio-media`).

---

## 🛠️ Step-by-Step Deployment Instructions

### 1. Create a Cloudflare Tunnel
1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com/) -> **Networks / Zero Trust** -> **Access** -> **Tunnels**.
2. Click **Create a Tunnel**, select **Cloudflare Tunnel (cloudflared)**, and give it a name (e.g., `portfolio-tunnel`).
3. Save the generated **Tunnel Token** (`eyJh...`).
4. Under **Public Hostname Page**:
   - Subdomain/Domain: `yourdomain.com` (or `@`)
   - Service Type: `HTTP`
   - URL: `web:8000`

### 2. Create a Cloudflare R2 Bucket
1. Go to **Cloudflare Dashboard** -> **R2 Storage** -> **Create Bucket** (name: `portfolio-media`).
2. Go to **R2 API Tokens** -> **Create API Token** with `Object Read & Write` permissions.
3. Note down:
   - Access Key ID
   - Secret Access Key
   - Endpoint URL (`https://<ACCOUNT_ID>.r2.cloudflarestorage.com`)
   - Custom Domain (optional: `media.yourdomain.com`)

### 3. Configure Production Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in the `.env` values:
```env
DEBUG=False
SECRET_KEY=your-strong-50-character-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,.trycloudflare.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://*.trycloudflare.com

CLOUDFLARE_TUNNEL_TOKEN=eyJh...your_token_here...
CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_key
CLOUDFLARE_R2_BUCKET_NAME=portfolio-media
CLOUDFLARE_R2_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
CLOUDFLARE_R2_CUSTOM_DOMAIN=media.yourdomain.com

POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=your_secure_db_password
POSTGRES_DB=portfolio_db
DATABASE_URL=postgres://<username>:<password>@db:5432/<dbname>
```

### 4. Deploy via Docker Compose
Run the stack using Docker Compose:
```bash
docker compose up -d --build
```

### 5. Run Database Migrations & Create Production Admin
Execute Django commands inside the web container:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

---

## 🔒 Security Hardening Verification

1. **Cloudflare IP Real Extraction**: `main/middleware.py` automatically extracts `HTTP_CF_CONNECTING_IP` to ensure accurate rate limiting and security logging without spoofing.
2. **Security Headers**: HSTS (1 year), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and Content Security Policy are strictly enforced.
3. **Debug Endpoints Restricted**: Development debug views (`cloudinary_test`, `cloudinary_debug`, `cloudinary_upload_test`, `test_social_links`) require `DEBUG=True` or staff authorization and return HTTP 403 Forbidden in production.
4. **Custom Admin URL**: Obfuscated admin path configured via `ADMIN_URL` environment variable.

---

## 🧪 Testing Health Endpoint
Verify application health:
```bash
curl -I https://yourdomain.com/health/
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-07-27T18:45:00.000000+00:00",
  "database": "OK",
  "debug": false,
  "storage": "Configured"
}
```

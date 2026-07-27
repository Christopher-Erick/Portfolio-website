# 📐 Technical Architecture & Design Document

## System Architecture

The Cybersecurity Professional Portfolio is a high-performance Django web application designed for zero-trust edge deployment behind Cloudflare.

```
[ Browser / Client ] 
        │ (HTTPS)
        ▼
[ Cloudflare Edge ] (DNS, WAF, DDoS Protection, SSL/TLS, Caching)
        │
        ▼ (Encrypted Cloudflare Tunnel / cloudflared)
[ Gunicorn WSGI Server ] (Python 3.12, Django 5.2.6)
        │
        ├──► [ PostgreSQL Database ] (Persistent Data Storage)
        │
        └──► [ Cloudflare R2 Bucket ] (Media / Document Storage via S3 API)
```

## Security Pipeline (Middleware Chain)

1. **SecurityMiddleware**: Django built-in SSL & security configuration.
2. **WhiteNoiseMiddleware**: Optimized static file serving with aggressive caching headers.
3. **SecurityHeadersMiddleware**: Enforces Content Security Policy (CSP), HSTS, X-Frame-Options (`DENY`), X-Content-Type-Options (`nosniff`), Referrer Policy.
4. **RateLimitMiddleware**: IP-based rate limiting using `HTTP_CF_CONNECTING_IP` header from Cloudflare.
5. **SecurityLoggingMiddleware**: Real-time logging of suspicious URL patterns, directory traversal attempts, and admin access.
6. **BlockSuspiciousRequestsMiddleware**: Active blocking of malicious security scanner user agents and SQL injection patterns.

## Application Modules

- **`main`**: Home, About, Resume, Contact form handling, Security dashboard, and Health check.
- **`portfolio`**: Project showcase, writeup documents, category/technology filtering, and detail views.
- **`blog`**: Technical blog post listing, detail view, unique IP view counter, and like/dislike feedback.
